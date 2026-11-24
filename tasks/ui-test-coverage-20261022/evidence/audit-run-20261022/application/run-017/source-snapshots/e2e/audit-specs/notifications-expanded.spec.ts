import { test, expect } from '../support/audit-fixture.js';
import { fixtureAccess } from '../support/local-app.js';
import { fixtureCategory, fixtureTile, loginCatalog } from '../support/catalog-app.js';

test.use({ auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES', auditFixture:'Actual React snackbar sanitization and error fallback. Controlled service errors and SystemJS exception. A click recorder captures mailto links and prevents external mail-client launch. No email is sent.' });

for(const n of [22,39,40]){
 const id=`UX-${String(n).padStart(3,'0')}`;
 test(`${id} actual snackbar rendering`,async({page,audit})=>{
  await audit.defineCase(id);
  const text=n===22?'START-'+'A'.repeat(1988)+'-END!!':n===39?'<img src=x onerror=alert(1)>':'<b>Save failed</b>';
  const dialogs:string[]=[];
  const alert=page.getByTestId('MicroWebUI_base_snackbar').locator('.MuiSnackbarContent-root[role="alert"]');
  const scrolling=alert.locator('.MuiSnackbarContent-message');
  await audit.step(1,async()=>{
   page.on('dialog',async dialog=>{dialogs.push(dialog.type());await dialog.dismiss();});
   await page.route('**/api/auth/v2/sso/extend',route=>route.fulfill({status:200,headers:{'single-ui-authorization':fixtureAccess()},json:{result:true}}));
   await loginCatalog(page);
   await page.route('**/api/audit/error',route=>route.fulfill({status:400,json:{message:text}}));
   await audit.record('error-fixture',{message:text,characters:text.length,scriptDialogRecorderInstalled:true});
  });
  await audit.step(2,async()=>{
   await page.evaluate(async()=>{const m=await (window as any).System.import('@fm/base');try{await m.Service.postService('/audit/error',{});}catch{ /* Real Axios handler has already dispatched this fixture error. */ }});
   await expect(alert).toBeVisible();
  });
  await audit.step(3,async()=>{
   if(n===22){await expect(alert).toHaveText(text);}
   else if(n===39){expect(dialogs).toEqual([]);await audit.record('script-dialog-events',dialogs);}
   else await expect(alert).toContainText('Save failed');
  });
  if(n===39) await audit.step(4,async()=>{await expect(page.getByRole('img',{name:'Markets Operations One logo',exact:true})).toBeVisible();});
  if(n===22){
   const markerVisible=async(end:boolean)=>scrolling.evaluate((node,end)=>{
    const textNode=node.querySelector('span')!.firstChild!;const range=document.createRange();
    range.setStart(textNode,end?textNode.textContent!.length-6:0);range.setEnd(textNode,end?textNode.textContent!.length:6);
    const marker=range.getBoundingClientRect(),box=node.getBoundingClientRect();
    return marker.top>=box.top-1&&marker.bottom<=box.bottom+1&&marker.left>=box.left-1&&marker.right<=box.right+1;
   },end);
   await audit.step(4,async()=>{await scrolling.evaluate(node=>{node.scrollTop=0;});});
   await audit.step(5,async()=>{expect(await markerVisible(false)).toBe(true);});
   await audit.step(6,async()=>{await scrolling.evaluate(node=>{node.scrollTop=node.scrollHeight;});});
   await audit.step(7,async()=>{expect(await markerVisible(true)).toBe(true);});
  }
 });
}

for(const n of [41,42]){
 const id=`UX-${String(n).padStart(3,'0')}`;
 test(`${id} actual support email link`,async({page,audit})=>{
  await audit.defineCase(id);let captured:string|null=null;
  const stack=n===41?'SECRET-TEST':'line1 & line2 # ?';
  const contact=page.getByTestId('FallbackError__page-id').getByRole('link',{name:'Contact PSS',exact:true});
  await audit.step(1,async()=>{
   await page.route('**/api/auth/v2/sso/extend',route=>route.fulfill({status:200,headers:{'single-ui-authorization':fixtureAccess()},json:{result:true}}));
   const app=await loginCatalog(page,{drawers:[fixtureCategory([fixtureTile()])]});
   await page.route('**/audit-fixtures/test-container.js',route=>route.fulfill({contentType:'application/javascript',
    body:`System.register([],function(e){return{execute:function(){e('default',function(){var x=new Error('Controlled support error');x.stack=${JSON.stringify(stack)};throw x;});}}});`}));
   await page.evaluate(()=>{
    (window as any).__capturedMail=[];
    document.addEventListener('click',event=>{const a=(event.target as Element).closest('a');if(a?.href.startsWith('mailto:')){event.preventDefault();(window as any).__capturedMail.push(a.href);}},true);
   });
   await app.openDrawer();await app.clickCard();await expect(contact).toBeVisible();
  });
  await audit.step(2,async()=>{await contact.click();captured=await page.evaluate(()=>(window as any).__capturedMail[0]??null);expect(captured).not.toBeNull();await audit.record('captured-mailto',{href:captured,externalClientLaunched:false});});
  await audit.step(3,async()=>{
   const url=new URL(captured!);
   if(n===41)expect(url.searchParams.get('body')??'').not.toContain('SECRET-TEST');
   else expect(url.pathname).toBe('support@example.test');
  });
  if(n===42)await audit.step(4,async()=>{const url=new URL(captured!);expect(url.searchParams.getAll('body')).toEqual([stack]);});
 });
}
