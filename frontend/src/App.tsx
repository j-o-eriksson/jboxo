import { useEffect, useState } from "react";
import { addVideoData, fetchInfo } from "./utils";

type Video = {
  name: string;
  path: string;
};

type VideoInfo = {
  name: string;
  subtitles: string;
  duration: string;
};

const Main = () => {
  const [users, setUsers] = useState<Video[]>([]);
  const [info, setInfo] = useState<VideoInfo>({
    name: "-",
    subtitles: "-",
    duration: "-",
  });

  const fetchData = async () => {
    const response = await fetch("/videos");
    const { data } = await response.json();
    setUsers(data);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div>
      <MyList users={users} callback={setInfo} />
      <Info info={info} />
      <MyElement />
    </div>
  );
};

type ListProps = {
  users: Video[];
  callback: React.Dispatch<React.SetStateAction<VideoInfo>>;
};

const MyList: React.FC<ListProps> = ({ users, callback }) => {
  return (
    <ul>
      {users.map((user) => (
        <li
          key={user.name}
          onClick={async () => {
            await addVideoData(user.path);
            await fetchInfo(callback);
          }}
        >
          {user.name}
        </li>
      ))}
    </ul>
  );
};

const MyElement = () => {
  return (
    <div>
      <p />
      Hello!
    </div>
  );
};

const Info: React.FC<{ info: VideoInfo }> = ({ info }) => {
  return (
    <p>
      name: {info.name}
      <br />
      subtitles: {info.subtitles}
      <br />
      duration: {info.duration}
    </p>
  );
};

export default Main;
