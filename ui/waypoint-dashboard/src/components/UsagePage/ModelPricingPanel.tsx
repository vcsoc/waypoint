"use client";

import { useQuery } from "@tanstack/react-query";
import { Card } from "@/components/ui/card";
import { LineChart } from "@/components/shared/charts/line_chart";
import { createApiClient } from "@/lib/http/client";
import { getAuthHeaderName } from "@/lib/http/runtime";
import type { components } from "@/lib/http/schema";
import { formatDate, getProxyBaseUrl } from "@/components/networking";
import { EMPTY_DAILY_ACTIVITY_RESPONSE, reportingTimezone, toDailyData } from "./dailyActivityApi";

type Report = components["schemas"]["ModelPricingReport"];
const client = createApiClient({ getBaseUrl: getProxyBaseUrl, getAuthHeaderName });
const dollars = (value: number) => new Intl.NumberFormat(undefined, {
  style: "currency", currency: "USD", maximumFractionDigits: 4,
}).format(value);

export function ModelPricingPanel({ accessToken, startTime, endTime }: {
  accessToken: string; startTime: Date; endTime: Date;
}) {
  const timezone = reportingTimezone();
  const start = formatDate(startTime);
  const end = formatDate(endTime);
  const query = useQuery({
    queryKey: ["model-pricing", accessToken, start, end, timezone],
    queryFn: () => client.get<Report>("/model-pricing", {
      accessToken, query: { start_date: start, end_date: end, timezone_name: timezone },
    }),
  });
  if (query.isPending) return <Card className="p-5">Loading API-equivalent pricing...</Card>;
  if (query.isError || !query.data) return <Card className="p-5">API-equivalent pricing is unavailable</Card>;
  const report = query.data;
  const data = toDailyData(EMPTY_DAILY_ACTIVITY_RESPONSE, { startTime, endTime }).map((day) => ({
    date: day.date,
    "API-equivalent value": (report.daily ?? []).filter((row) => row.date === day.date)
      .reduce((total, row) => total + (row.estimated_cost ?? 0), 0),
  }));
  return <Card className="space-y-4 p-5">
    <div>
      <h3 className="font-medium">API-equivalent value</h3>
      <p className="text-2xl font-semibold">{report.estimated_cost === null || report.estimated_cost === undefined
        ? "No priced usage" : dollars(report.estimated_cost)}</p>
      <p className="text-sm text-muted-foreground">
        What successful requests would cost at current API token rates. Actual spend and budgets are unchanged.
        Failed requests, internal calls and gateway cache hits are excluded.
      </p>
      {(report.missing_rate_requests ?? 0) > 0 && <p className="text-sm text-amber-700">
        Partial estimate: {report.missing_rate_requests} requests have no published pricing rate
      </p>}
    </div>
    <LineChart data={data} index="date" categories={["API-equivalent value"]} valueFormatter={dollars} />
    <details>
      <summary className="cursor-pointer text-sm font-medium">API-equivalent model rates ({report.pricing.length} models)</summary>
      <p className="my-3 text-sm text-muted-foreground">
        USD per million tokens. Local Qwen 2B and 4B use hosted Qwen 3.5 9B as a benchmark, not an exact-model price.
      </p>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead><tr><th>Model</th><th>Input</th><th>Cached input</th><th>Output</th><th>Selected-range value</th><th>Pricing reference</th></tr></thead>
          <tbody>{report.pricing.map((price) => {
            const tier = price.tiers[0];
            const rows = (report.daily ?? []).filter((row) => row.model_name === price.model_name);
            const value = rows.reduce((total, row) => total + (row.estimated_cost ?? 0), 0);
            return <tr key={price.model_name} className="border-t">
              <td className="py-2">{price.model_name}</td>
              <td>{tier ? dollars(tier.input_per_token * 1_000_000) : "Unavailable"}</td>
              <td>{tier ? dollars(tier.cached_input_per_token * 1_000_000) : "Unavailable"}</td>
              <td>{tier ? dollars(tier.output_per_token * 1_000_000) : "Unavailable"}</td>
              <td>{tier ? dollars(value) : "Unavailable"}</td>
              <td>{price.catalog_model}{price.basis === "hosted_qwen_benchmark" && " (benchmark)"}
                {price.source?.startsWith("https://") && <a className="ml-2 underline" href={price.source}
                  target="_blank" rel="noreferrer">Source</a>}
                {price.tiers.length > 1 && <span className="ml-2">Higher rates apply to long-context requests</span>}
              </td>
            </tr>;
          })}</tbody>
        </table>
      </div>
    </details>
  </Card>;
}
