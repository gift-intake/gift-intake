import * as React from "react";
import createClient from "openapi-fetch";
import { paths } from "../../lib/api/v1";
import { Button } from "@/components/ui/button";

interface AppProps {
  title: string;
}

const client = createClient<paths>({ baseUrl: "http://127.0.0.1:8000" });

const App: React.FC<AppProps> = ({ title }) => {
  const [healthData, setHealthData] = React.useState<any>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  const checkHealth = async () => {
    setLoading(true);
    setError(null);

    try {
      const { data, error: apiError } = await client.GET("/api/v1/health", {});
      if (apiError) {
        throw new Error("API returned an error");
      }
      setHealthData(data);
    } catch (err) {
      setError("Failed to connect to health endpoint");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    checkHealth();
  }, []);

  return (
    <div>
      <h2 className="text-amber-400 text-9xl">{title}</h2>
      <div>
        <h3>Health Check Test</h3>

        {loading && <p>Loading...</p>}

        {error && (
          <div>
            <p>Error: {error}</p>
            <Button onClick={checkHealth}>Retry</Button>
          </div>
        )}

        {!loading && !error && healthData && (
          <div>
            <p>Status: {JSON.stringify(healthData)}</p>
            <Button onClick={checkHealth}>Refresh</Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
