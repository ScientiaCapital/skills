# Demo Execution Playbook — Objection Handling Matrix (LAER)

> Extracted from SKILL.md — content preserved verbatim.

#### **Higher Ed: "We already use [LMS]. Will Pearl integrate?"**
- **Listen:** Let them name the LMS (Kaltura, Panopto, Canvas, Blackboard).
- **Acknowledge:** "Your LMS is your hub. We need to work within that ecosystem."
- **Explore:** "Does your LMS have a public API or webhook for ingestion?" / "How does content get into your LMS today?"
- **Respond:** "Pearl outputs to RTMP/SRT/MP4. If your LMS accepts [that format], we connect directly. If not, we use a bridge like Kaltura's API. Let me check our integrations doc and send you the specific recipe for [LMS name] by EOD." (Don't make it up—verify post-demo.)

#### **Courts/Legal: "Matrox was working. Why change?"**
- **Listen:** "So you've had Matrox for a while. What was the experience?"
- **Acknowledge:** "Matrox was solid. But here's the issue—Matrox exited the market 2 years ago. No more updates, no vendor support, no compliance patches."
- **Explore:** "When your current Matrox hardware fails, what's your plan? Secondhand eBay? Or do you need a modern vendor?"
- **Respond:** "Pearl-2 is the compliance-hardened replacement. It records locally + cloud with full audit trails. Let me send you our legal compliance brief. It maps Pearl to your current Matrox workflow." (Show feature parity.)

#### **Corporate AV: "Our Zoom Rooms ecosystem handles this."**
- **Listen:** "Tell me how Zoom Rooms works for you today."
- **Acknowledge:** "Zoom Rooms is great for cloud meetings. But recording and NDI streaming is where we add value."
- **Explore:** "Do you record every meeting today? And do you need low-latency streaming to your offices without cloud hops?"
- **Respond:** "Zoom Rooms excels at the meeting experience. Pearl excels at capture + local NDI streaming + multi-room management. Think of it as the recording + streaming layer under your Zoom Rooms. We enhance, not compete." (Positioning: complementary, not competitor.)

#### **Government: "We can't use cloud. Period."**
- **Listen:** Don't push back. Hear the constraint.
- **Acknowledge:** "Got it. On-prem only. That's a hard requirement for FIPS/NIST compliance."
- **Explore:** "Can Pearl record and stream locally on your network? That's where we excel. Are you open to on-prem Epiphan Connect, or strictly Pearl with zero cloud?"
- **Respond:** "Pearl records to local SSD. RTMP/SRT outputs to your on-prem server. Optional: Epiphan Connect as a Docker container in your data center. You control all data. Let me demo that setup." (Pivot to on-prem flow.)

#### **Healthcare/K-12: "This is too expensive."**
- **Listen:** "What price were you expecting?"
- **Acknowledge:** "I hear cost is a concern. Let's talk about ROI."
- **Explore:** "Today, how much do you spend on [technician time / manual recording / compliance audits / LMS licenses]? And what's your payback timeline?"
- **Respond:** "One Pearl Mini ($X) + Epiphan Connect ($Y/year) replaces your current [system] and saves you [# hours/month] of tech time. That's [Z] payback in [# months]. Here's the full ROI model." (Have a ROI doc ready. Don't wing it.)
