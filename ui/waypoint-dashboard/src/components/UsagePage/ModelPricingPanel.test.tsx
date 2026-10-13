import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { ModelPricingPanel } from "./ModelPricingPanel";
import type { components } from "@/lib/http/schema";

const get = vi.hoisted(() => vi.fn());
vi.mock("@/lib/http/client", () => ({ createApiClient: () => ({ get }) }));
vi.mock("@/components/shared/charts/line_chart", () => ({ LineChart: () => null }));

type Report = components["schemas"]["ModelPricingReport"];
const report: Report = {
  currency: "USD",
  pricing: [{ currency: "USD", model_name: "local-qwen3.5-4b", catalog_model: "hosted-qwen-reference", basis: "hosted_qwen_benchmark",
    source: "https://example.test/pricing", tiers: [{ above_tokens: 0, input_per_token: 0.000001,
      output_per_token: 0.000002, cached_input_per_token: 0.000001 }] }],
  daily: [{ date: "2026-01-02", model_name: "local-qwen3.5-4b", estimated_cost: 12,
    estimated_requests: 3, missing_rate_requests: 0 }],
  estimated_cost: 12, estimated_requests: 3, missing_rate_requests: 0,
};

function show() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(<QueryClientProvider client={client}>
    <ModelPricingPanel accessToken="test-token" startTime={new Date(2026, 0, 1)} endTime={new Date(2026, 0, 2)} />
  </QueryClientProvider>);
}

describe("API-equivalent pricing", () => {
  it("shows a separate estimate and labels local Qwen rates as a benchmark", async () => {
    get.mockResolvedValue(report);
    show();
    expect((await screen.findAllByText(/12\.00/)).length).toBeGreaterThan(0);
    expect(screen.getByText(/Actual spend and budgets are unchanged/)).toBeInTheDocument();
    expect(screen.getByText(/hosted-qwen-reference \(benchmark\)/)).toBeInTheDocument();
    expect(screen.getByText(/not an exact-model price/)).toBeInTheDocument();
    expect(get).toHaveBeenCalledWith("/model-pricing", expect.objectContaining({ query: {
      start_date: "2026-01-01", end_date: "2026-01-02", timezone_name: Intl.DateTimeFormat().resolvedOptions().timeZone,
    } }));
  });

  it("does not present unknown rates as zero-cost usage", async () => {
    const unavailable = { ...report, estimated_cost: null, missing_rate_requests: 3,
      pricing: [{ ...report.pricing[0], tiers: [], basis: "unavailable" }] };
    get.mockResolvedValue(unavailable);
    show();
    expect(await screen.findByText("No priced usage")).toBeInTheDocument();
    expect(screen.getByText(/Partial estimate: 3 requests/)).toBeInTheDocument();
    expect(screen.getAllByText("Unavailable")).toHaveLength(4);
  });

  it("shows a failure instead of retaining stale estimates", async () => {
    get.mockRejectedValue(new Error("offline"));
    show();
    expect(await screen.findByText("API-equivalent pricing is unavailable")).toBeInTheDocument();
    expect(screen.queryByText(/12\.00/)).not.toBeInTheDocument();
  });
});
