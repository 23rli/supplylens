const questions = [
  "What's our biggest stockout risk right now?",
  "Which supplier should I be most concerned about?",
  "What immediate actions should I take this week?",
  "Which SKUs have both low stock and an unreliable primary supplier?",
];

/**
 * Props: { onSelect: (question: string) => void }
 * Shown when chat has no messages. Clicking a question fires it.
 */
export default function SuggestedQuestions({ onSelect }) {
  return (
    <div className="flex flex-col items-center justify-center h-full gap-6 text-center px-4">
      <div>
        <div className="w-14 h-14 bg-blue-600/20 border border-blue-500/30 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <span className="text-2xl">🔍</span>
        </div>
        <h3 className="text-slate-100 font-semibold text-lg mb-1">Ask SupplyLens AI</h3>
        <p className="text-slate-400 text-sm max-w-md">
          Grounded on live inventory and supplier data. Ask anything about risk, suppliers, or recommended actions.
        </p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-xl">
        {questions.map((q) => (
          <button
            key={q}
            onClick={() => onSelect(q)}
            className="text-left px-4 py-3 bg-slate-700 hover:bg-slate-600 border border-slate-600 hover:border-slate-500 rounded-xl text-sm text-slate-300 hover:text-slate-100 transition-all"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
