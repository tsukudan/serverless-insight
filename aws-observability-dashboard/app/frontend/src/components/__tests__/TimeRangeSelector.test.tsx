import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import TimeRangeSelector from "@/components/TimeRangeSelector";

describe("TimeRangeSelector", () => {
  it("4つのボタンが表示される（1h, 6h, 24h, 7d）", () => {
    render(<TimeRangeSelector value="1h" onChange={vi.fn()} />);
    expect(screen.getByText("1h")).toBeInTheDocument();
    expect(screen.getByText("6h")).toBeInTheDocument();
    expect(screen.getByText("24h")).toBeInTheDocument();
    expect(screen.getByText("7d")).toBeInTheDocument();
  });

  it("ボタンクリックで onChange が呼ばれる", () => {
    const onChange = vi.fn();
    render(<TimeRangeSelector value="1h" onChange={onChange} />);
    fireEvent.click(screen.getByText("24h"));
    expect(onChange).toHaveBeenCalledWith("24h");
  });
});
