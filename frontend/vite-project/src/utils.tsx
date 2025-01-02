import React from "react";

export type InfoCallback = React.Dispatch<React.SetStateAction<VideoInfo>>;
export type TabCallback = React.Dispatch<React.SetStateAction<string>>;

export type Video = {
  id: number;
  name: string;
  path: string;
  duration: string;
  thumbnail: string;
};

export type Subtitle = {
  id: number;
  name: string;
}

export type VideoInfo = {
  name: string;
  subtitles: string;
  duration: number;
  thumbnail: string;
};

export function getDefaultInfo(): VideoInfo {
  return {
    name: "-",
    subtitles: "-",
    duration: 0,
    thumbnail: "-",
  };
}

export const fetchData = async (endpoint: string, callback: any) => {
  const response = await fetch(endpoint);
  const data = await response.json();
  callback(data);
};

export const fetchInfo = async (callback: any) => {
  const response = await fetch("/api/selected");
  const info = await response.json();
  console.log(info)
  callback({
    name: info.name,
    subtitles: info.subtitle_name,
    duration: info.duration.toString(),
    thumbnail: info.thumbnail,
  });
};

const postBase = async (endpoint: string, body: any = {}) => {
  const response = await fetch(endpoint, {
    method: "POST",
    body: JSON.stringify(body),
  });
  const text = await response.text();
  console.log(`Post request to ${endpoint} returned: ${text}`);
};

export const addVideoData = async (dataType: string, asset_id: number) => {
  return postBase("/api/control/add", { type: dataType, id: asset_id })
};

export const playVideo = async (seek_time: number = 0) => {
  return postBase("/api/control/play", { seek_time: seek_time });
};

export const pauseVideo = async () => {
  return postBase("/api/control/pause");
};

export const stopVideo = async () => {
  return postBase("/api/control/stop");
};

export const wakeScreen = async () => {
  return postBase("/api/control/wake");
};
