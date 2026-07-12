import { useEffect, useState } from "react";

export function useDomainPayload<T>(embedded: T | null, loader: () => Promise<T>) {
  const [data, setData] = useState<T | null>(embedded);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (embedded) {
      setData(embedded);
      setError(null);
      return;
    }

    let cancelled = false;
    loader()
      .then((payload) => {
        if (!cancelled) {
          setData(payload);
          setError(null);
        }
      })
      .catch((reason: Error) => {
        if (!cancelled) {
          setError(reason.message);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [embedded, loader]);

  return { data, error, setData };
}
