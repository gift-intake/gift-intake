import { FileUp } from "lucide-react";
import "./App.css";
import FileUpload from "./components/FileUpload";
import DisplayResults from "./components/DisplayResults";

function App() {
  return (
    <div className="h-screen flex flex-col items-center justify-center p-4">
      <DisplayResults
        fileName="example.pdf"
        extractedText="This is the extracted text from the PDF file. It will be displayed here."
      />
      <div className="mt-8 flex flex-col items-center">
        <h2 className="text-lg font-semibold mb-2">Display</h2>
        <FileUpload />
      </div>
    </div>
  );
}

export default App;
