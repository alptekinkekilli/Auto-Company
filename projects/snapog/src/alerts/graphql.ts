// Cloudflare Analytics GraphQL client — thin wrapper.
// Docs: https://developers.cloudflare.com/analytics/graphql-api/
// Only used to fetch R2 bucket storage bytes. D1-derived metrics do not
// require this API.

const CLOUDFLARE_GRAPHQL_ENDPOINT = 'https://api.cloudflare.com/client/v4/graphql';

export interface R2StorageSample {
  bucketName: string;
  payloadSizeBytes: number;
  metadataSizeBytes: number;
}

// Returns null on any failure (token missing, network, GraphQL error).
// Callers must treat null as "unknown" and skip the storage check rather
// than firing a false alert.
export async function fetchR2BucketStorage(
  accountId: string,
  bucketName: string,
  apiToken: string
): Promise<R2StorageSample | null> {
  const query = `
    query R2Storage($accountTag: String!, $bucketName: String!) {
      viewer {
        accounts(filter: { accountTag: $accountTag }) {
          r2StorageAdaptiveGroups(
            filter: { bucketName: $bucketName }
            limit: 1
            orderBy: [datetime_DESC]
          ) {
            max { payloadSize metadataSize }
            dimensions { bucketName }
          }
        }
      }
    }`;

  let resp: Response;
  try {
    resp = await fetch(CLOUDFLARE_GRAPHQL_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiToken}`,
      },
      body: JSON.stringify({
        query,
        variables: { accountTag: accountId, bucketName },
      }),
    });
  } catch (err) {
    console.error('[alerts] R2 GraphQL fetch failed:', err);
    return null;
  }

  if (!resp.ok) {
    console.error(`[alerts] R2 GraphQL HTTP ${resp.status}: ${await resp.text().catch(() => '')}`);
    return null;
  }

  let json: {
    data?: {
      viewer?: {
        accounts?: Array<{
          r2StorageAdaptiveGroups?: Array<{
            max?: { payloadSize?: number; metadataSize?: number };
            dimensions?: { bucketName?: string };
          }>;
        }>;
      };
    };
    errors?: Array<{ message: string }>;
  };
  try {
    json = await resp.json();
  } catch {
    return null;
  }

  if (json.errors?.length) {
    console.error('[alerts] R2 GraphQL errors:', JSON.stringify(json.errors));
    return null;
  }

  const group = json.data?.viewer?.accounts?.[0]?.r2StorageAdaptiveGroups?.[0];
  if (!group) return null;

  return {
    bucketName: group.dimensions?.bucketName ?? bucketName,
    payloadSizeBytes: group.max?.payloadSize ?? 0,
    metadataSizeBytes: group.max?.metadataSize ?? 0,
  };
}
