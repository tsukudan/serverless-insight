import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import ErrorMessage from "@/components/ErrorMessage";

describe("ErrorMessage", () => {
  it("エラーメッセージが表示される", () => {
    render(<ErrorMessage message="データの取得に失敗しました" />);
    expect(screen.getByText("データの取得に失敗しました")).toBeInTheDocument();
  });
});
