import { createBrowserRouter } from "react-router-dom";
import Root from "./components/Root";
import Chatrooms from "./routes/Chatrooms";
import Home from "./routes/Home";
import NotFound from "./routes/NotFound";
import RefBooks from "./routes/RefBooks";
import RefData from "./routes/RefData";
import SystemInfo from "./routes/systemInfo";
import Users from "./routes/Users";
import WebSocketChat from "./routes/WebSocketChat";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <NotFound />,
    children: [
      {
        path: "",
        element: <Home />,
      },
      {
        path: "books",
        element: <RefBooks />,
      },
      {
        path: "data",
        element: <RefData />,
      },
      {
        path: "system-info",
        element: <SystemInfo />,
      },
      {
        path: "chatrooms",
        element: <Chatrooms />,
      },
      {
        path: "chattings/:chatroomPk",
        element: <WebSocketChat />,
      },
    ],
  },
]);

export default router;
