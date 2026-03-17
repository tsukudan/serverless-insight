import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import EndpointsTable from "@/components/EndpointsTable";
import { EndpointMetrics } from "@/types";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
  usePathname: () => "/",
}));

const mockEndpoints: EndpointMetrics[] = [
  {
    endpoint: "GET /posts",
    requests: 150,
    successRate: 98.5,
    avgLatency: 45.2,
    p95Latency: 120.0,
    errors: 2,
  },
  {
    endpoint: "POST /posts",
    requests: 30,
    successRate: 100.0,
    avgLatency: 80.1,
    p95Latency: 200.5,
    errors: 0,
  },
];

describe("EndpointsTable", () => {
  it("空配列の時に「表示するエンドポイントがありません」が表示される", () => {
    render(<EndpointsTable endpoints={[]} />);
    expect(
      screen.getByText("表示するエンドポイントがありません")
    ).toBeInTheDocument();
  });

  it("データがある場合テーブルが表示される", () => {
    render(<EndpointsTable endpoints={mockEndpoints} />);
    expect(screen.getByRole("table")).toBeInTheDocument();
  });

  it("エンドポイント名が表示される", () => {
    render(<EndpointsTable endpoints={mockEndpoints} />);
    expect(screen.getByText("GET /posts")).toBeInTheDocument();
    expect(screen.getByText("POST /posts")).toBeInTheDocument();
  });
});
