import React from "react";
import useServices from "../../../services";
import useDispatcher from "../../../hooks/dispathcer";
import { getEnv } from "../../../utils/common";
import { validateLoginRequest } from "../../../auth/validation";

const useController = () => {
  const { dispacthLoading, dispacthErrorMessage } = useDispatcher();
  const [loading, setLoading] = React.useState(false);
  const [username, setUsername] = React.useState<string>();
  const [password, setPassword] = React.useState<string>();
  const { login, loginEntra } = useServices();
  const [code, setCode] = React.useState<string>();
  // To be removed after entra migration done
  const [client_id, setClient_id] = React.useState<string>();
  const [iss, setIss] = React.useState<string>();
  const [value, setValue] = React.useState(0);
  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };
  React.useEffect(() => {
    dispacthLoading(false);
    const params = new URLSearchParams(window.location.search);
    const checkCode = params.get("code");
    if (checkCode) {
      setCode(checkCode);
      setIss(params.get("iss") ?? undefined);
      setClient_id(params.get("client_id") ?? undefined);
      setUsername(undefined);
      setPassword(undefined);
    }
  }, []);
  React.useEffect(() => {
    if (code) {
      onLogin({ code, iss, client_id });
    }
  }, [code, iss, client_id]);

  const onLogin = async (input: unknown) => {
    dispacthErrorMessage(undefined);
    const validation = validateLoginRequest(input);
    if (!validation.success) {
      dispacthErrorMessage("Enter valid login credentials.");
      return;
    }
    const data = validation.data;
    setLoading(true);
    try {
      // if only code exist, consider it as entra sso login, otherwise use normal login,
      // this is for compatibility during migration, will remove the code check after migration
      const isEntraSSO =
        "code" in data && data.code && !data.iss && !data.client_id;
      if (isEntraSSO) {
        // only support entra sso
        await loginEntra(data);
      } else {
        await login(data);
      }
    } catch (_error) {
      dispacthErrorMessage("Login failed, please try again.");
    } finally {
      setLoading(false);
    }
  };
  const onLoginUserNamePassword = () => {
    onLogin({ username: username ?? "", password: password ?? "" });
  };
  const onKeyUp = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.code === "Enter") {
      onLoginUserNamePassword();
    }
  };
  const onKeyUpPassword = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.code === "Enter") {
      onLoginUserNamePassword();
    }
  };
  const showNormalLogin = React.useMemo(() => {
    if (["PROD"].includes(getEnv())) {
      const params = new URLSearchParams(window.location.search);
      const showNormalLogin = params.get("show_normal_login");
      if (showNormalLogin === null || !["Y", "y"].includes(showNormalLogin)) {
        return false;
      }
    }
    return true;
  }, []);

  return {
    username,
    setUsername,
    password,
    setPassword,
    onLogin,
    onLoginUserNamePassword,
    handleChange,
    value,
    onKeyUp,
    loading,
    showNormalLogin,
    onKeyUpPassword,
  };
};

export default useController;
