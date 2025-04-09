import * as React from "react";
import Header from "./Header";
import HeroList, { HeroListItem } from "./HeroList";
import TextInsertion from "./TextInsertion";
import { makeStyles } from "@fluentui/react-components";
import { Ribbon24Regular, LockOpen24Regular, DesignIdeas24Regular } from "@fluentui/react-icons";
import { getEmailSubject } from "../taskpane";
import TextDisplay from "./TextDisplay";
import createClient from "openapi-fetch";
import { paths } from "../../lib/api/v1";

interface AppProps {
  title: string;
}

const useStyles = makeStyles({
  root: {
    minHeight: "100vh",
  },
});

const client = createClient<paths>({ baseUrl: "http://127.0.0.1:8000" });

const App: React.FC<AppProps> = ({ title }) => {
  const styles = useStyles();
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
    <div className={styles.root}>
      <h2>{title}</h2>
      <div>
        <h3>Health Check Test</h3>

        {loading && <p>Loading...</p>}

        {error && (
          <div>
            <p>Error: {error}</p>
            <button onClick={checkHealth}>Retry</button>
          </div>
        )}

        {!loading && !error && healthData && (
          <div>
            <p>Status: {JSON.stringify(healthData)}</p>
            <button onClick={checkHealth}>Refresh</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
