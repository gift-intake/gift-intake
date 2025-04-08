import React, { useEffect, useState } from "react";
import { Button, Field, Textarea, tokens, makeStyles } from "@fluentui/react-components";




const TextDisplay = () => {
  const [subject, setSubject] = useState("Loading...");
  Office.context.mailbox.item.body.getAsync(
    "text",
    { asyncContext: "This is passed to the callback" },
    function callback(result) {
      setSubject(result.value);
       
    });

  // useEffect(() => {
  //   Office.onReady(async (info) => {
  //     if (info.host === Office.HostType.Outlook) {
  //       const subjectText = await props.getText(subject);
  //       setSubject(subjectText);
  //     }
  //   });
  // }, []);


  return (
    <div style={{ padding: "1rem" }}>
      <h2>Email Body</h2>
      <p>{subject}</p>
      {/* <Textarea size="large" value={subject}/> */}
      
    </div>
  );
}

export default TextDisplay