import * as React from "react";
import createClient from "openapi-fetch";
import { components, paths } from "../../lib/api/v1";
import { Button } from "@/components/ui/button";
import DisplayResults from "./DisplayResults";
import { useEffect } from "react";

const client = createClient<paths>({ baseUrl: "http://127.0.0.1:8000" });

export default function App() {
  const [emailBody, setEmailBody] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState<boolean>(false);
  const [results, setResults] = React.useState<
    components["schemas"]["InferenceResponseData"] | null
  >(null);
  const [attachments, setAttachments] = React.useState<Office.AttachmentDetails[]>([]);
  const [attachmentResults, setAttachmentResults] = React.useState<{
    [id: string]: {
      loading: boolean;
      error: string | null;
      data: components["schemas"]["InferenceResponseData"] | null;
    };
  }>({});

  const processEmailText = async (text: string) => {
    try {
      setLoading(true);
      const { data, error: apiError } = await client.POST("/api/v1/display/extract-text", {
        body: {
          text: text,
        },
      });

      if (apiError) {
        throw new Error(`API Error: ${JSON.stringify(apiError)}`);
      }

      setResults(data);
    } catch (err) {
<<<<<<< HEAD
      setError(`Failed to process email: ${err instanceof Error ? err.message : String(err)}`);
=======
      setError("Failed to connect to health endpoint ${err.message}");
>>>>>>> 65158328 (set up)
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAttachments = () => {
    return new Promise<Office.AttachmentDetails[]>((resolve, reject) => {
      try {
        // Use the direct property access approach instead of async method
        const msgAttach = Office.context.mailbox.item.attachments;
        const attachmentsList = [];

        if (msgAttach && msgAttach.length > 0) {
          for (let i = 0; i < msgAttach.length; i++) {
            attachmentsList.push({
              ...msgAttach[i],
              contentType: msgAttach[i].contentType || "application/octet-stream",
            });
          }
          resolve(attachmentsList);
        } else {
          console.log("No attachments found or attachments property not available");
          resolve([]);
        }
      } catch (error) {
        console.error("Error accessing attachments:", error);
        reject(
          new Error(
            `Failed to access attachments: ${error instanceof Error ? error.message : String(error)}`
          )
        );
      }
    });
  };

  const getAttachmentContent = (attachment: Office.AttachmentDetails) => {
    return new Promise<string>((resolve, reject) => {
      Office.context.mailbox.item.getAttachmentContentAsync(attachment.id, (result) => {
        if (result.status === Office.AsyncResultStatus.Succeeded) {
          resolve(result.value.content);
        } else {
          reject(new Error(`Failed to get attachment content: ${result.error.message}`));
        }
      });
    });
  };

  const processAttachment = async (attachment: Office.AttachmentDetails) => {
    try {
      // Update state to show loading for this attachment
      setAttachmentResults((prev) => ({
        ...prev,
        [attachment.id]: { loading: true, error: null, data: null },
      }));

      // Get attachment content as base64
      const base64Content = await getAttachmentContent(attachment);

      // Convert base64 to Blob
      const contentType = attachment.contentType || "application/octet-stream";
      const byteCharacters = atob(base64Content);
      const byteArrays = [];

      for (let offset = 0; offset < byteCharacters.length; offset += 1024) {
        const slice = byteCharacters.slice(offset, offset + 1024);
        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
          byteNumbers[i] = slice.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
      }

      const blob = new Blob(byteArrays, { type: contentType });
      const file = new File([blob], attachment.name, { type: contentType });

      // Create FormData and append file
      const formData = new FormData();
      formData.append("file", file);

      // Use fetch directly instead of the typed client for file uploads
      const response = await fetch("http://127.0.0.1:8000/api/v1/display/extract-file", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = (await response.json()) as components["schemas"]["InferenceResponseData"];

      setAttachmentResults((prev) => ({
        ...prev,
        [attachment.id]: { loading: false, error: null, data },
      }));
    } catch (err) {
      setAttachmentResults((prev) => ({
        ...prev,
        [attachment.id]: {
          loading: false,
          error: `Failed to process attachment: ${err instanceof Error ? err.message : String(err)}`,
          data: null,
        },
      }));
      console.error(err);
    }
  };

  const processAllAttachments = async () => {
    try {
      const attachmentsList = await fetchAttachments();
      setAttachments(attachmentsList);

      // Process each attachment in parallel
      await Promise.all(attachmentsList.map(processAttachment));
    } catch (err) {
      setError(
        `Failed to process attachments: ${err instanceof Error ? err.message : String(err)}`
      );
      console.error(err);
    }
  };

  useEffect(() => {
    Office.context.mailbox.item.body.getAsync("text", async (bodyResult) => {
      if (bodyResult.status === Office.AsyncResultStatus.Succeeded) {
        const emailText = bodyResult.value;
        setEmailBody(emailText);

        // Automatically process the email as soon as we have the body
        await processEmailText(emailText);
        await processAllAttachments();
      } else {
        setError(`Failed to get email body: ${bodyResult.error.message}`);
        setLoading(false);
      }
    });
  }, []);

  return (
    <div className="p-4">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {loading && (
        <div className="flex flex-col items-center justify-center space-y-2">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-700"></div>
          <div className="text-gray-600">Processing email...</div>
        </div>
      )}

      {/* {!loading && !results && emailBody && (
        <div className="bg-gray-50 p-4 border rounded">
          <h3 className="text-lg font-medium mb-2">Email Content</h3>
          <pre className="whitespace-pre-wrap">{emailBody}</pre>
        </div>
      )} */}

      {!loading && results && emailBody && (
        <div className="mt-8">
        <h3 className="text-lg font-medium mb-4">Email Content</h3>
        <DisplayResults data={results} />
      </div>
        
        )}

      {attachments.length > 0 && (
        <div className="mt-8">
          <h3 className="text-lg font-medium mb-4">Attachments</h3>
          <div className="space-y-6">
            {attachments.map((attachment) => {
              const result = attachmentResults[attachment.id];

              return (
                <div key={attachment.id}>
                  {result?.loading && (
                    <div className="flex items-center space-x-2 my-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-700"></div>
                      <div className="text-gray-600">Processing...</div>
                    </div>
                  )}

                  {result?.error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded my-2">
                      {result.error}
                    </div>
                  )}

                  {result?.data && <DisplayResults data={result.data} />}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

// const App: React.FC<AppProps> = ({ title }) => {
//   const [healthData, setHealthData] = React.useState<any>(null);
//   const [loading, setLoading] = React.useState(true);
//   const [error, setError] = React.useState<string | null>(null);

//   const checkHealth = async () => {
//     setLoading(true);
//     setError(null);

//     try {
//       const { data, error: apiError } = await client.GET("/api/v1/health", {});
//       if (apiError) {
//         throw new Error("API returned an error");
//       }
//       setHealthData(data);
//     } catch (err) {
//       setError("Failed to connect to health endpoint");
//       console.error(err);
//     } finally {
//       setLoading(false);
//     }
//   };

//   React.useEffect(() => {
//     checkHealth();
//   }, []);

//   return (
//     <div>
//       <h2 className="text-amber-400 text-9xl">{title}</h2>
//       <DisplayResults data={sampleData} />
//       {/* <div>
//         <h3>Health Check Test</h3>

//         {loading && <p>Loading...</p>}

//         {error && (
//           <div>
//             <p>Error: {error}</p>
//             <Button onClick={checkHealth}>Retry</Button>
//           </div>
//         )}

//         {!loading && !error && healthData && (
//           <div>
//             <p>Status: {JSON.stringify(healthData)}</p>
//             <Button onClick={checkHealth}>Refresh</Button>
//           </div>
//         )}
//       </div> */}
//     </div>
//   );
// };

// export default App;
