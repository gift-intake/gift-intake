import { useDropzone } from "react-dropzone";
import { cn } from "@/lib/utils";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { File, UploadCloud } from "lucide-react";

type FileUploadProps = React.ComponentProps<typeof Card>;

export default function FileUpload({ className, ...props }: FileUploadProps) {
  const [files, setFiles] = useState<File[]>([]);

  const { getRootProps, getInputProps } = useDropzone({
    accept: { "application/pdf": [".pdf"] },
    onDrop: (acceptedFiles) => setFiles(acceptedFiles),
    multiple: true,
  });

  return (
    <Card
      className={cn("w-[380px] shadow-md hover:shadow-lg transition-shadow", className)}
      {...props}
    >
      <CardHeader>
        <CardTitle>Upload File</CardTitle>
        <CardDescription>Drag and drop your files.</CardDescription>
      </CardHeader>
      <CardContent>
        <div
          {...getRootProps()}
          className="border-2 border-dashed border-gray-300 rounded-lg p-10 flex flex-col items-center justify-center cursor-pointer hover:border-gray-500"
        >
          <input {...getInputProps()} />
          <UploadCloud className="w-10 h-10 text-gray-400" />
          <p className="text-gray-500">Drop files here or click to upload</p>
        </div>

        {files.length > 0 && (
          <ul className="mt-4 space-y-2">
            {files.map((file) => {
              const truncatedName =
                file.name.length > 25 ? file.name.slice(0, 25) + "..." : file.name;

              return (
                <li key={file.name} className="flex items-center gap-2 text-sm text-gray-700">
                  <File className="w-4 h-4 text-gray-400" />
                  <span>{truncatedName}</span>
                </li>
              );
            })}
          </ul>
        )}
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button variant="outline" onClick={() => setFiles([])}>
          Cancel
        </Button>
        <Button>Upload</Button>
      </CardFooter>
    </Card>
  );
}
