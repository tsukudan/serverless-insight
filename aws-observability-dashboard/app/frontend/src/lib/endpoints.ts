/** エンドポイントスラッグのマッピング定義 */
export const ENDPOINT_SLUGS: Record<string, string> = {
  "get-posts": "GET /posts",
  "post-posts": "POST /posts",
  "get-posts-id": "GET /posts/{id}",
  "delete-posts-id": "DELETE /posts/{id}",
};

/** エンドポイント名からスラッグに変換 */
export function endpointToSlug(endpoint: string): string {
  const entry = Object.entries(ENDPOINT_SLUGS).find(
    ([, value]) => value === endpoint
  );
  if (entry) return entry[0];

  // マッピングにない場合はフォールバック変換
  return endpoint
    .toLowerCase()
    .replace(/[{}]/g, "")
    .replace(/\//g, "-")
    .replace(/\s+/g, "-")
    .replace(/^-+|-+$/g, "")
    .replace(/-+/g, "-");
}

/** スラッグからエンドポイント名に逆変換 */
export function slugToEndpoint(slug: string): string | undefined {
  return ENDPOINT_SLUGS[slug];
}
