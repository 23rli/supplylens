const questions = [
  "What's our biggest stockout risk right now?",
  "Which supplier should I be most concerned about?",
  "What immediate actions should I take this week?",
  "Which SKUs have low stock and an unreliable supplier?",
];

export default function SuggestedQuestions({ onSelect }) {
  return (
    <div className="flex flex-col items-center justify-center h-full gap-6 text-center px-4">
      <div>
        <div className="w-12 h-12 bg-brand-50 border border-brand-100 rounded-2xl flex items-center justify-center mx-auto mb-3 text-brand-600 font-semibold">AI</div>
        <h3 className="text-ink font-semibold text-base mb-1">Ask SupplyLens AI</h3>
        <p className="text-ink-soft text-sm max-w-md">Grounded on live inventory and supplier data. Ask about risk, suppliers, or recommended actions.</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-xl">
        {questions.map((q) => (
          <button key={q} onClick={() => onSelect(q)}
            className="text-left px-4 py-3 bg-white border border-surface-border hover:border-brand-500 hover:bg-brand-50 rounded-xl text-sm text-ink-soft hover:text-ink transition-all">
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
