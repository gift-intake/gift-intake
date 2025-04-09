import * as React from "react";
import createClient from "openapi-fetch";
import { paths } from "../../lib/api/v1";

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
      setError("Failed to connect to health endpoint ${err.message}");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    checkHealth();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h2 className="text-4xl text-red-600 mb-4">{title}</h2>
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <h3 className="text-2xl font-semibold text-gray-700 mb-4">Health Check</h3>

        {loading && <p className="text-gray-600">Loading...</p>}

        {error && (
          <div className="text-red-500 mb-4">
            <p>Error: {error}</p>
            <button
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              onClick={checkHealth}
            >
              Retry
            </button>
          </div>
        )}

        {!loading && !error && healthData && (
          <div>
            <p className="text-green-500 font-bold">Status:</p>
            <p className="text-gray-700">{JSON.stringify(healthData)}</p>
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4"
              onClick={checkHealth}
            >
              Refresh
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
