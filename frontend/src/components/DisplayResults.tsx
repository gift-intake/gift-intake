import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

interface DisplayResultsProps {
  fileName: string;
  extractedText: string;
}
export default function DisplayResults({ fileName, extractedText }: DisplayResultsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Results</CardTitle>
        <CardDescription>{fileName}</CardDescription>
      </CardHeader>

      <CardContent className="overflow-y-auto max-h-96">
        <pre className="whitespace-pre-wrap">{extractedText}</pre>
      </CardContent>
    </Card>
  );
}
