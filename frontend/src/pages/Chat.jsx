import ChatPanel from "../components/ChatPanel";

export default function Chat() {
  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">AI Supply Chain Analyst</h1>
        <p className="text-slate-400 text-sm mt-1">
          Natural language risk analysis · grounded on live inventory and supplier data
        </p>
      </div>
      <ChatPanel />
    </div>
  );
}
