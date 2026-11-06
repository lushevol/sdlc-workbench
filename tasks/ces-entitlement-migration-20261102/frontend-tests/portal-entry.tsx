// Actual base App and shared authenticator. The remote upper application is an isolated contract consumer.
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from '../../../repos/ui/mfe-base/src/App';
import * as Hooks from '../../../repos/ui/mfe-base/src/hooks';
import * as Dispatcher from '../../../repos/ui/mfe-base/src/hooks/dispathcer';
import * as LoginUtil from '../../../repos/ui/mfe-base/src/utils/login';
import * as Auth from '../../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator';

const bridge = window as any;
bridge.__base = { Hooks, Dispatcher, LoginUtil };
bridge.__auth = Auth;
const Consumer = (props: any) => {
  const dispatcher = Dispatcher.default();
  React.useEffect(() => { bridge.__dispatcher = dispatcher; });
  const code = props.parameters.permissionCode ?? 'feature-a:action-a';
  const allowed = Auth.hasPermission(code);
  return <section data-testid={`consumer-${props.parameters.label}`}>
    <h2>{props.parameters.label}</h2>
    <button disabled={!allowed}>Export fixture data</button>
    <output data-testid="scope">{props.entitlementScope?.tileId ?? 'missing'}</output>
  </section>;
};
bridge.System = { import: async (name: string) => {
  if (name === '@fixture/consumer') return { default: Consumer };
  throw new Error(`Unexpected remote module: ${name}`);
} };
createRoot(document.getElementById('root')!).render(<App version="CES_LOCAL_CONTROLLED" />);
