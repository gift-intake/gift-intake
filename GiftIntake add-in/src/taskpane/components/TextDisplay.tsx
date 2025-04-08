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

    const msgCC = Office.context.mailbox.item.cc;
   

    const msgAttach = Office.context.mailbox.item.attachments;
    const attachments = [];
    if(msgAttach.length>0){
      for(let i = 0; i < msgAttach.length; i++){
        attachments.push(msgAttach[i].name);
      }
    }else{
      attachments.push("This email doesn't contain any attachments.");
    }
    
    const msgTo = Office.context.mailbox.item.to;

  return (
    <div style={{ padding: "1rem" }}>
    <h2>Email To</h2>
      <p>
        <ul>
        {msgTo.map((item) =>{
          return <li>{item.displayName}: {item.emailAddress}</li>
        })}
        </ul>
      </p>
      <h2>Email Cc</h2>
      <p>
        <ul>
        {msgCC.map((item) =>{
          return <li>{item.displayName} :{item.emailAddress}</li>
        })}
        </ul>
      </p>

      <h2>Email Body</h2>
      <p>{subject}</p>

      <h2>Email Attachments</h2>
      <p>
        <ul>
        {attachments.map((item) =>{
          return <li> {item}</li>
        })}
        </ul>
      </p>      
    </div>
  );
}

export default TextDisplay