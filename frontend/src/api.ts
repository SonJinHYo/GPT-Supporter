import axios from "axios";
import Cookie from "js-cookie";

interface ISignUpVariables {
  email: string;
  password: string;
  username: string;
}
interface ISignInVariables {
  username: string;
  password: string;
}
const instance = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1/",
  withCredentials: true,
});

instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("jwt");

    if (token) {
      config.headers["jwt"] = token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const signUp = ({ email, password, username }: ISignUpVariables) =>
  instance
    .post(
      `users/signup`,
      { email, password, username },
      {
        headers: {
          "X-CSRFToken": Cookie.get("csrftoken") || "",
        },
      }
    )
    .then((response) => response.status);

export const signIn = ({ username, password }: ISignInVariables) =>
  instance
    .post(
      `users/signin`,
      { username, password },
      {
        headers: {
          "X-CSRFToken": Cookie.get("csrftoken") || "",
        },
      }
    )
    .then((response) => {
      const token = response.data.token;
      localStorage.setItem("jwt", token);
    });

export const getMe = () =>
  instance.get(`users/me`).then((response) => response.data);
