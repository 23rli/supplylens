import ChatPanel from "../components/ChatPanel";
import { PageHeader } from "../components/ui";

export default function Chat() {
  return (
    <div className="space-y-5">
      <PageHeader title="AI Analyst" subtitle="Natural-language risk analysis · grounded on live inventory and supplier data" />
      <ChatPanel />
    </div>
  );
}
