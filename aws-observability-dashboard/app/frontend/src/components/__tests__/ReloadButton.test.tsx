import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import ReloadButton from "@/components/ReloadButton";

describe("ReloadButton", () => {
  it("クリックで onClick が呼ばれる", () => {
    const onClick = vi.fn();
    render(<ReloadButton onClick={onClick} loading={false} />);
    fireEvent.click(screen.getByText("リロード"));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it("loading=true の時 disabled になる", () => {
    render(<ReloadButton onClick={vi.fn()} loading={true} />);
    expect(screen.getByText("リロード").closest("button")).toBeDisabled();
  });
});
