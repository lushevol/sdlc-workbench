# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: notifications-expanded.spec.ts >> UX-042 actual support email link
- Location: e2e/audit-specs/notifications-expanded.spec.ts:49:2

# Error details

```
Error: expect(received).toEqual(expected) // deep equality

- Expected  - 1
+ Received  + 1

  Array [
-   "line1 & line2 # ?",
+   "line1 ",
  ]
```

# Page snapshot

```yaml
- generic [ref=e4]:
  - generic [ref=e7]:
    - img "Markets Operations One logo" [ref=e9]
    - generic [ref=e10]:
      - generic [ref=e11] [cursor=pointer]:
        - img "new tile" [ref=e13]
        - generic [ref=e14]: New Tile
      - generic [ref=e15]:
        - img "dark" [ref=e17]
        - generic [ref=e19]:
          - text: dark
          - checkbox "Theme Switch" [ref=e22] [cursor=pointer]
      - group [ref=e26]:
        - generic [ref=e27]: 06:10 UTC
        - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
      - button "User Profiles" [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button "Share Feedback" [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist "workspaces" [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region "Test Tile Demo" [ref=e48]:
          - textbox "Workspace Name" [ref=e52]: Test Tile Demo
      - button "Add Workspace" [ref=e54] [cursor=pointer]
    - tabpanel [ref=e59]:
      - generic [ref=e62]:
        - heading "There is a problem in this Tile." [level=6] [ref=e63]
        - paragraph [ref=e64]: Please click the button below to send the Error detail to the Application Support Team.
        - link "Contact PSS" [active] [ref=e66] [cursor=pointer]:
          - /url: "mailto:support@example.test?subject=Error in localhost&body=line1 & line2 # ?"
```

# Test source

```ts
  1  | import { test, expect } from '../support/audit-fixture.js';
  2  | import { fixtureAccess } from '../support/local-app.js';
  3  | import { fixtureCategory, fixtureTile, loginCatalog } from '../support/catalog-app.js';
  4  | 
  5  | test.use({ auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES', auditFixture:'Actual React snackbar sanitization and error fallback. Controlled service errors and SystemJS exception. A click recorder captures mailto links and prevents external mail-client launch. No email is sent.' });
  6  | 
  7  | for(const n of [22,39,40]){
  8  |  const id=`UX-${String(n).padStart(3,'0')}`;
  9  |  test(`${id} actual snackbar rendering`,async({page,audit})=>{
  10 |   await audit.defineCase(id);
  11 |   const text=n===22?'START-'+'A'.repeat(1988)+'-END!!':n===39?'<img src=x onerror=alert(1)>':'<b>Save failed</b>';
  12 |   const dialogs:string[]=[];
  13 |   const alert=page.getByTestId('MicroWebUI_base_snackbar').locator('.MuiSnackbarContent-root[role="alert"]');
  14 |   const scrolling=alert.locator('.MuiSnackbarContent-message');
  15 |   await audit.step(1,async()=>{
  16 |    page.on('dialog',async dialog=>{dialogs.push(dialog.type());await dialog.dismiss();});
  17 |    await page.route('**/api/auth/v2/sso/extend',route=>route.fulfill({status:200,headers:{'single-ui-authorization':fixtureAccess()},json:{result:true}}));
  18 |    await loginCatalog(page);
  19 |    await page.route('**/api/audit/error',route=>route.fulfill({status:400,json:{message:text}}));
  20 |    await audit.record('error-fixture',{message:text,characters:text.length,scriptDialogRecorderInstalled:true});
  21 |   });
  22 |   await audit.step(2,async()=>{
  23 |    await page.evaluate(async()=>{const m=await (window as any).System.import('@fm/base');try{await m.Service.postService('/audit/error',{});}catch{ /* Real Axios handler has already dispatched this fixture error. */ }});
  24 |    await expect(alert).toBeVisible();
  25 |   });
  26 |   await audit.step(3,async()=>{
  27 |    if(n===22){await expect(alert).toHaveText(text);}
  28 |    else if(n===39){expect(dialogs).toEqual([]);await audit.record('script-dialog-events',dialogs);}
  29 |    else await expect(alert).toContainText('Save failed');
  30 |   });
  31 |   if(n===39) await audit.step(4,async()=>{await expect(page.getByRole('img',{name:'Markets Operations One logo',exact:true})).toBeVisible();});
  32 |   if(n===22){
  33 |    const markerVisible=async(end:boolean)=>scrolling.evaluate((node,end)=>{
  34 |     const textNode=node.querySelector('span')!.firstChild!;const range=document.createRange();
  35 |     range.setStart(textNode,end?textNode.textContent!.length-6:0);range.setEnd(textNode,end?textNode.textContent!.length:6);
  36 |     const marker=range.getBoundingClientRect(),box=node.getBoundingClientRect();
  37 |     return marker.top>=box.top-1&&marker.bottom<=box.bottom+1&&marker.left>=box.left-1&&marker.right<=box.right+1;
  38 |    },end);
  39 |    await audit.step(4,async()=>{await scrolling.evaluate(node=>{node.scrollTop=0;});});
  40 |    await audit.step(5,async()=>{expect(await markerVisible(false)).toBe(true);});
  41 |    await audit.step(6,async()=>{await scrolling.evaluate(node=>{node.scrollTop=node.scrollHeight;});});
  42 |    await audit.step(7,async()=>{expect(await markerVisible(true)).toBe(true);});
  43 |   }
  44 |  });
  45 | }
  46 | 
  47 | for(const n of [41,42]){
  48 |  const id=`UX-${String(n).padStart(3,'0')}`;
  49 |  test(`${id} actual support email link`,async({page,audit})=>{
  50 |   await audit.defineCase(id);let captured:string|null=null;
  51 |   const stack=n===41?'SECRET-TEST':'line1 & line2 # ?';
  52 |   const contact=page.getByTestId('FallbackError__page-id').getByRole('link',{name:'Contact PSS',exact:true});
  53 |   await audit.step(1,async()=>{
  54 |    await page.route('**/api/auth/v2/sso/extend',route=>route.fulfill({status:200,headers:{'single-ui-authorization':fixtureAccess()},json:{result:true}}));
  55 |    const app=await loginCatalog(page,{drawers:[fixtureCategory([fixtureTile()])]});
  56 |    await page.route('**/audit-fixtures/test-container.js',route=>route.fulfill({contentType:'application/javascript',
  57 |     body:`System.register([],function(e){return{execute:function(){e('default',function(){var x=new Error('Controlled support error');x.stack=${JSON.stringify(stack)};throw x;});}}});`}));
  58 |    await page.evaluate(()=>{
  59 |     (window as any).__capturedMail=[];
  60 |     document.addEventListener('click',event=>{const a=(event.target as Element).closest('a');if(a?.href.startsWith('mailto:')){event.preventDefault();(window as any).__capturedMail.push(a.href);}},true);
  61 |    });
  62 |    await app.openDrawer();await app.clickCard();await expect(contact).toBeVisible();
  63 |   });
  64 |   await audit.step(2,async()=>{await contact.click();captured=await page.evaluate(()=>(window as any).__capturedMail[0]??null);expect(captured).not.toBeNull();await audit.record('captured-mailto',{href:captured,externalClientLaunched:false});});
  65 |   await audit.step(3,async()=>{
  66 |    const url=new URL(captured!);
  67 |    if(n===41)expect(url.searchParams.get('body')??'').not.toContain('SECRET-TEST');
  68 |    else expect(url.pathname).toBe('support@example.test');
  69 |   });
> 70 |   if(n===42)await audit.step(4,async()=>{const url=new URL(captured!);expect(url.searchParams.getAll('body')).toEqual([stack]);});
     |                                                                                                               ^ Error: expect(received).toEqual(expected) // deep equality
  71 |  });
  72 | }
  73 | 
```