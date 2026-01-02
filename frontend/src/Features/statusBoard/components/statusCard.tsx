import { StatusCardData } from "../utils/utils";

export default function StatusCard() {
  return (
    <>
      {StatusCardData.map((card) => (
        <article
          key={card.status}
          className="flex items-start space-x-3 border border-gray-200 bg-white p-3 rounded-2xl shadow-sm w-64 min-w-64"
        >
          <div className={`h-4 w-4 rounded-full mt-1 ${card.indicator}`} />
          <div>
            <h3 className="font-semibold text-sm text-gray-800">{card.status}</h3>
            <p className="text-xs text-gray-500">{card.desc}</p>
          </div>
        </article>
      ))}
    </>
  );
}
