import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import SummaryCard from "@/components/SummaryCard";

describe("SummaryCard", () => {
  it("タイトルと値が表示される", () => {
    render(<SummaryCard title="総リクエスト数" value={1234} />);
    expect(screen.getByText("総リクエスト数")).toBeInTheDocument();
    expect(screen.getByText("1234")).toBeInTheDocument();
  });

  it("unit が渡された場合に表示される", () => {
    render(<SummaryCard title="平均レイテンシ" value={45.2} unit="ms" />);
    expect(screen.getByText("ms")).toBeInTheDocument();
  });

  it("unit が渡されない場合は表示されない", () => {
    render(<SummaryCard title="エラー率" value="2.5" />);
    const container = screen.getByText("2.5").closest("div");
    expect(container).not.toHaveTextContent("ms");
  });
});
