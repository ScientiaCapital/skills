# Twilio Voice Webhooks Reference

Production patterns extracted from VozLux voice platform.

## Webhook Endpoints Overview

```python
from fastapi import FastAPI, Request, Depends
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather, Connect, Stream
from twilio.rest import Client

app = FastAPI(title="Voice AI Phone Integration")
```

## Incoming Call Webhook

### Universal Endpoint (Multi-Tenant)

Routes calls by looking up the destination phone number in database:

```python
@app.post("/voice/incoming")
async def incoming_call_universal(
    request: Request,
    _validated: bool = Depends(validate_twilio_request)
):
    """
    Universal webhook for incoming calls - routes by phone number.

    Flow:
    1. Caller dials your Twilio number
    2. Twilio POSTs with To=your_number
    3. Lookup phone number in database
    4. Get business_id and agent_type
    5. Route to correct agent with context
    """
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    from_number = form_data.get("From")
    to_number = form_data.get("To")  # The Twilio number that was called

    # Lookup phone number to get business context
    phone_config = await lookup_phone_number(to_number)

    if not phone_config or not phone_config.is_active:
        response = VoiceResponse()
        response.say(
            "Lo sentimos, este numero no esta configurado. "
            "Sorry, this number is not configured.",
            voice='Polly.Lupe'
        )
        response.hangup()
        return Response(content=str(response), media_type="application/xml")

    # Auto-detect language from caller number
    _, _, default_lang = get_language_preference(from_number)

    # Route based on tier
    if phone_config.plan_type in ("pro", "enterprise"):
        # Use Media Streams for low latency
        return route_to_media_streams(phone_config, default_lang)
    else:
        # Use TwiML + Polly for starter tier
        return await handle_incoming_call(call_sid, from_number, phone_config)
```

### Language Auto-Detection from Caller Number

```python
def get_language_preference(caller_number: str) -> tuple[str, str, str]:
    """
    Determine language based on caller's phone number country code.

    Args:
        caller_number: E.164 format (+15128771367, +5215512345678)

    Returns:
        Tuple of (greeting_text, first_language, default_language)

    Strategy:
    - Mexico (+52): Spanish first, default Spanish
    - US/Canada (+1): English first, default English
    - Unknown: Spanish first (majority customer base)
    """
    if not caller_number:
        return (
            "Para espanol, presione uno. For English, press two.",
            "es",
            "es"
        )

    number = caller_number.strip()

    if number.startswith("+52"):
        # Mexico - Spanish first
        return (
            "Para espanol, presione uno. For English, press two.",
            "es",
            "es"
        )
    elif number.startswith("+1"):
        # US/Canada - English first
        return (
            "For English, press one. Para espanol, presione dos.",
            "en",
            "en"
        )
    else:
        # International/Unknown - Spanish first
        return (
            "Para espanol, presione uno. For English, press two.",
            "es",
            "es"
        )
```

## Media Streams WebSocket Setup

For PRO/ENTERPRISE tier with real-time audio streaming:

### TwiML Response for Media Streams

```python
def route_to_media_streams(phone_config, language: str) -> Response:
    """Connect call to Media Streams WebSocket for low-latency audio."""
    response = VoiceResponse()

    base_url = os.environ.get("BASE_URL", "your-app.railway.app")
    ws_url = (
        f"wss://{base_url}/voice/media-stream/"
        f"{phone_config.business_id}/{phone_config.agent_type}"
        f"?lang={language}&tier={phone_config.plan_type}"
    )

    connect = Connect()
    stream = Stream(url=ws_url)
    connect.append(stream)
    response.append(connect)

    return Response(content=str(response), media_type="application/xml")
```

### WebSocket Handler

```python
from fastapi import WebSocket, WebSocketDisconnect
import json
import base64
import asyncio

@app.websocket("/voice/media-stream/{business_id}/{agent_type}")
async def media_stream_websocket(
    websocket: WebSocket,
    business_id: str,
    agent_type: str,
    lang: str = "en",
    tier: str = "pro"
):
    """
    WebSocket endpoint for Twilio Media Streams.

    Provides real-time bidirectional audio streaming
    with STT and TTS for sub-600ms latency.

    TwiML to connect:
        <Connect>
            <Stream url="wss://your-app/voice/media-stream/..." />
        </Connect>
    """
    await websocket.accept()

    # Initialize pipeline and state
    stream_sid = None
    call_sid = None
    is_running = True
    send_queue = asyncio.Queue()

    try:
        while is_running:
            message = await websocket.receive_text()
            data = json.loads(message)
            event_type = data.get("event")

            if event_type == "connected":
                # Initial connection established
                protocol = data.get("protocol", "unknown")
                print(f"Media Streams connected: protocol={protocol}")

            elif event_type == "start":
                # Stream starting with metadata
                start_data = data.get("start", {})
                stream_sid = start_data.get("streamSid")
                call_sid = start_data.get("callSid")

                media_format = start_data.get("mediaFormat", {})
                encoding = media_format.get("encoding", "audio/x-mulaw")
                sample_rate = media_format.get("sampleRate", 8000)

                # Send greeting audio here
                await send_greeting(websocket, stream_sid, language=lang)

            elif event_type == "media":
                # Incoming audio chunk from caller
                media_data = data.get("media", {})
                payload = media_data.get("payload")

                if payload:
                    audio_bytes = base64.b64decode(payload)
                    # Process through STT -> Agent -> TTS
                    response_audio = await process_audio(audio_bytes)

                    if response_audio:
                        await send_audio(websocket, stream_sid, response_audio)

            elif event_type == "stop":
                # Stream ending
                reason = data.get("stop", {}).get("reason", "unknown")
                print(f"Media Stream stopping: reason={reason}")
                is_running = False

    except WebSocketDisconnect:
        print("Media Streams WebSocket disconnected")
    finally:
        # Cleanup
        pass
```

### Sending Audio Back to Caller

```python
async def send_audio(websocket: WebSocket, stream_sid: str, audio_data: bytes):
    """Send audio chunk back to Twilio."""
    payload = base64.b64encode(audio_data).decode("utf-8")

    message = {
        "event": "media",
        "streamSid": stream_sid,
        "media": {
            "payload": payload,
        }
    }

    await websocket.send_text(json.dumps(message))
```

### Clear Audio Queue (For Interruption Support)

```python
async def send_clear(websocket: WebSocket, stream_sid: str):
    """
    Clear queued audio on Twilio's side.
    Use for barge-in/interruption support.
    """
    message = {
        "event": "clear",
        "streamSid": stream_sid,
    }

    await websocket.send_text(json.dumps(message))
```

### Send Mark Event

```python
async def send_mark(websocket: WebSocket, stream_sid: str, name: str):
    """
    Send mark event to track audio playback position.
    Twilio will notify when mark is reached.
    """
    message = {
        "event": "mark",
        "streamSid": stream_sid,
        "mark": {
            "name": name,
        }
    }

    await websocket.send_text(json.dumps(message))
```

## Status Callbacks

Track call lifecycle events:

```python
@app.post("/voice/status/{call_sid}")
async def call_status(
    call_sid: str,
    request: Request,
    _validated: bool = Depends(validate_twilio_request)
):
    """
    Webhook for call status updates.

    Status values:
    - initiated: Call created
    - ringing: Ringing at destination
    - answered: Call connected
    - completed: Call ended normally
    - busy: Destination busy
    - no-answer: No answer
    - failed: Call failed
    - canceled: Call canceled
    """
    form_data = await request.form()
    status = form_data.get("CallStatus")
    duration = form_data.get("CallDuration")

    print(f"Call status update: {call_sid} -> {status}")

    if status in ["completed", "failed", "busy", "no-answer"]:
        await end_call(call_sid)

        # Update database with call outcome
        outcome_map = {
            "completed": "answered",
            "busy": "busy",
            "no-answer": "no_answer",
            "failed": "failed",
        }
        await log_call_outcome(call_sid, outcome_map.get(status, status), duration)

    return {"status": "ok"}
```

## Call Transfer to Human Agent

```python
def transfer_to_human(destination_number: str, caller_name: str = None) -> VoiceResponse:
    """
    Transfer call to human agent.

    Args:
        destination_number: Human agent's phone number
        caller_name: Optional caller name for announcement
    """
    response = VoiceResponse()

    # Announce transfer
    response.say(
        "Let me transfer you to someone who can help you better. Please hold.",
        voice='Polly.Joanna'
    )

    # Dial human agent with caller ID passthrough
    dial = response.dial(
        caller_id=settings.twilio_phone_number,
        timeout=30,
        action='/voice/transfer-complete'  # Callback when transfer completes
    )
    dial.number(destination_number)

    # If transfer fails, apologize
    response.say(
        "I apologize, the line is busy. Please try again later.",
        voice='Polly.Joanna'
    )

    return response
```

## Outbound Call Patterns

### Initiating Outbound Calls

```python
from twilio.rest import Client

def make_outbound_call(
    to_number: str,
    from_number: str,
    webhook_url: str,
    status_callback: str = None,
    lead_context: dict = None
) -> str:
    """
    Initiate an outbound call.

    Args:
        to_number: Destination phone number (E.164)
        from_number: Your Twilio number (E.164)
        webhook_url: URL for call handling when answered
        status_callback: URL for status updates
        lead_context: Context to pass to webhook via query params

    Returns:
        Call SID
    """
    client = Client(account_sid, auth_token)

    # Build webhook URL with context
    url = f"{webhook_url}?lang={lead_context.get('language', 'en')}"
    if lead_context.get('scheduled_call_id'):
        url += f"&scheduled_call_id={lead_context['scheduled_call_id']}"

    call = client.calls.create(
        to=to_number,
        from_=from_number,
        url=url,
        method='POST',
        status_callback=status_callback,
        status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
        status_callback_method='POST',
        timeout=30,  # Ring for 30 seconds
        machine_detection='Enable',  # Detect voicemail
        machine_detection_timeout=5
    )

    return call.sid
```

### Outbound Call Connect Webhook

```python
@app.post("/voice/outbound/connect/{agent_type}")
async def outbound_call_connect(
    agent_type: str,
    request: Request,
    scheduled_call_id: Optional[str] = Query(None),
    lang: str = Query("en"),
    _validated: bool = Depends(validate_twilio_request)
):
    """
    Webhook called when outbound call connects.
    Provides initial greeting to the prospect.
    """
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    call_status = form_data.get("CallStatus")
    answered_by = form_data.get("AnsweredBy")  # human, machine_start, etc.

    # Check if voicemail
    if answered_by and "machine" in answered_by:
        return await handle_voicemail(call_sid, agent_type, scheduled_call_id)

    # Fetch lead context from database
    lead_context = await get_lead_context(scheduled_call_id)

    # Create agent and get opening message
    agent = get_agent(agent_type, lead_context)
    opening = await agent.handle_call_start(call_context=lead_context)

    # Build response
    response = VoiceResponse()
    voice = "Polly.Lupe" if lang == "es" else "Polly.Joanna"
    speech_lang = "es-MX" if lang == "es" else "en-US"

    gather = Gather(
        input='speech',
        action=f'/voice/outbound/process/{call_sid}?lang={lang}',
        method='POST',
        language=speech_lang,
        speech_timeout='auto',
        enhanced=True
    )
    gather.say(opening, voice=voice, language=speech_lang)

    response.append(gather)

    # If no input, redirect
    response.redirect(
        f'/voice/outbound/connect/{agent_type}?scheduled_call_id={scheduled_call_id}&lang={lang}'
    )

    return Response(content=str(response), media_type="application/xml")
```

## Webhook Signature Validation

Always validate Twilio requests in production:

```python
from twilio.request_validator import RequestValidator
from functools import wraps

validator = None

def init_validator(auth_token: str, enforce: bool = True):
    """Initialize webhook signature validator."""
    global validator
    validator = RequestValidator(auth_token) if enforce else None

async def validate_twilio_request(request: Request) -> bool:
    """
    Dependency to validate Twilio webhook signatures.

    Usage:
        @app.post("/webhook")
        async def webhook(_validated: bool = Depends(validate_twilio_request)):
            ...
    """
    if validator is None:
        return True  # Validation disabled (development only)

    # Get signature from header
    signature = request.headers.get("X-Twilio-Signature", "")

    # Build full URL
    url = str(request.url)

    # Get POST params
    form_data = await request.form()
    params = dict(form_data)

    # Validate
    if not validator.validate(url, params, signature):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")

    return True
```

## TwiML Response Patterns

### Gather with Speech Recognition

```python
def create_gather_response(prompt: str, language: str = "en") -> VoiceResponse:
    """Create TwiML response that gathers speech input."""
    response = VoiceResponse()

    voice = 'Polly.Lupe' if language == "es" else 'Polly.Joanna'
    speech_lang = 'es-MX' if language == "es" else 'en-US'

    gather = Gather(
        input='speech',
        action='/voice/process',
        method='POST',
        language=speech_lang,
        speech_timeout='auto',
        enhanced=True  # Enable enhanced speech recognition
    )
    gather.say(prompt, voice=voice)

    response.append(gather)

    # Fallback if no input
    response.say("I didn't catch that. Goodbye!", voice=voice)
    response.hangup()

    return response
```

### DTMF Menu (IVR)

```python
def create_ivr_menu(language: str = "en") -> VoiceResponse:
    """Create IVR menu with DTMF input."""
    response = VoiceResponse()

    gather = Gather(
        input='dtmf',
        action='/voice/language-selected',
        method='POST',
        num_digits=1,
        timeout=5
    )

    if language == "en":
        gather.say(
            "For English, press one. Para espanol, presione dos.",
            voice='Polly.Joanna'
        )
    else:
        gather.say(
            "Para espanol, presione uno. For English, press two.",
            voice='Polly.Lupe'
        )

    response.append(gather)

    # Default if no input
    response.redirect('/voice/incoming?lang=en')

    return response
```

## Rate Limiting and Security

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/calls/outbound")
@limiter.limit("10/minute")
async def initiate_outbound_call(request: Request):
    """Rate-limited outbound call API."""
    ...
```

## Environment Variables

Required configuration:

```bash
# Twilio credentials
TWILIO_ACCOUNT_SID=ACxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+15551234567

# Application
BASE_URL=your-app.railway.app
VOZLUX_ENV=production  # or development

# Voice providers (choose one)
CARTESIA_API_KEY=...  # For TTS
DEEPGRAM_API_KEY=...  # For STT
```

## Error Handling Pattern

```python
async def handle_with_error_recovery(request: Request) -> Response:
    """Handle call with error recovery."""
    try:
        # Normal processing
        response = await process_call(request)
        return Response(content=str(response), media_type="application/xml")

    except Exception as e:
        logger.error(f"Error processing call: {e}")

        # Graceful error response
        response = VoiceResponse()
        response.say(
            "Lo sentimos, hubo un error. Por favor intente mas tarde. "
            "Sorry, there was an error. Please try again later.",
            voice='Polly.Lupe'
        )
        response.hangup()

        return Response(content=str(response), media_type="application/xml")
```

## Call Logging

Log calls to database for analytics:

```python
async def log_incoming_call(
    business_id: str,
    phone_number_id: str,
    call_sid: str,
    from_number: str,
    to_number: str,
    agent_type: str
):
    """Log incoming call to database."""
    await supabase.table("call_logs").insert({
        "business_id": business_id,
        "phone_number_id": phone_number_id,
        "twilio_call_sid": call_sid,
        "direction": "inbound",
        "from_number": from_number,
        "to_number": to_number,
        "agent_type": agent_type,
        "status": "initiated"
    }).execute()
```

## PII Redaction for Logs

Never log raw phone numbers:

```python
class PIIRedactor:
    """Redact PII for secure logging."""

    def redact(self, value: str) -> str:
        """Redact phone number for logging."""
        if not value or len(value) < 7:
            return "[REDACTED]"
        # Show last 4 digits only
        return f"***{value[-4:]}"

pii_redactor = PIIRedactor()

# Usage
logger.info(f"Call from {pii_redactor.redact(from_number)}")
# Output: "Call from ***1234"
```
