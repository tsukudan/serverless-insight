import { describe, it, expect } from "vitest";
import { endpointToSlug, slugToEndpoint } from "@/lib/endpoints";

describe("endpointToSlug", () => {
  it("GET /posts を get-posts に変換する", () => {
    expect(endpointToSlug("GET /posts")).toBe("get-posts");
  });

  it("POST /posts を post-posts に変換する", () => {
    expect(endpointToSlug("POST /posts")).toBe("post-posts");
  });

  it("GET /posts/{id} を get-posts-id に変換する", () => {
    expect(endpointToSlug("GET /posts/{id}")).toBe("get-posts-id");
  });

  it("DELETE /posts/{id} を delete-posts-id に変換する", () => {
    expect(endpointToSlug("DELETE /posts/{id}")).toBe("delete-posts-id");
  });
});

describe("slugToEndpoint", () => {
  it("get-posts を GET /posts に逆変換する", () => {
    expect(slugToEndpoint("get-posts")).toBe("GET /posts");
  });

  it("post-posts を POST /posts に逆変換する", () => {
    expect(slugToEndpoint("post-posts")).toBe("POST /posts");
  });

  it("get-posts-id を GET /posts/{id} に逆変換する", () => {
    expect(slugToEndpoint("get-posts-id")).toBe("GET /posts/{id}");
  });

  it("delete-posts-id を DELETE /posts/{id} に逆変換する", () => {
    expect(slugToEndpoint("delete-posts-id")).toBe("DELETE /posts/{id}");
  });

  it("未定義スラッグで undefined が返る", () => {
    expect(slugToEndpoint("unknown-endpoint")).toBeUndefined();
  });
});
