import { createBrowserRouter } from "react-router-dom";
import Root from "./components/Root";
import Chatrooms from "./routes/Chatrooms";
import CreatePublicScript from "./routes/CreatePublicScript";
import Dialogues from "./routes/Dialogues";
import Forbidden from "./routes/Forbbiden";
import Home from "./routes/Home";
import NotFound from "./routes/NotFound";
import PublicScripts from "./routes/PublicScripts";
import RefBooks from "./routes/RefBooks";
import RefData from "./routes/RefData";
import SystemInfo from "./routes/systemInfo";
import TipPage from "./routes/TipPage";
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
        path: "forbidden",
        element: <Forbidden />,
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
      {
        path: "system-info/:systemInfoPk/dialogues",
        element: <Dialogues />,
      },
      {
        path: "public-scripts",
        element: <PublicScripts />,
      },
      {
        path: process.env.REACT_APP_CREATE_PUBLIC_SCRIPT_URL,
        element: <CreatePublicScript />,
      },
      {
        path: "tip",
        element: <TipPage />,
      },
    ],
  },
]);

export default router;
