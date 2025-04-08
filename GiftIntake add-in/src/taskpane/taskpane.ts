/* global Office console */
export async function getEmailSubject() {
  return new Promise((resolve, reject) => {
    try {
      const item = Office.context.mailbox.item;
      if (item && item.subject) {
        item.subject.getAsync((result) => {
          if (result.status === Office.AsyncResultStatus.Succeeded) {
            resolve(result.value);
          } else {
            reject(result.error.message);
          }
        });
      } else {
        resolve("No subject available");
      }
    } catch (error) {
      reject("Error: " + error);
    }
  });
}

// export async function insertText(text: string) {
//   // Write text to the cursor point in the compose surface.
//   try {
//     Office.context.mailbox.item?.body.setSelectedDataAsync(
//       text,
//       { coercionType: Office.CoercionType.Text },
//       (asyncResult: Office.AsyncResult<void>) => {
//         if (asyncResult.status === Office.AsyncResultStatus.Failed) {
//           throw asyncResult.error.message;
//         }
//       }
//     );
//   } catch (error) {
//     console.log("Error: " + error);
//   }
// }
