export interface IUser {
  id: number;
  first_name: string,
  last_name: string,
  age: number,
  role: string,
  exp: string,
  stack: Array<string>
  pic?: URL
}

export interface ICourse {
  _id: number,
  name: string,
  desc: string,
  keywords: Array<string>,
  category: string,
  rating: number,
  count_views: number,
  rating: number,
  keywords: string[]
}

export type SkillContextType = {
  user: IUser | null;
  setUser: Dispatch<SetStateAction<IUser>>;
  courses: ICourse[];
  setCourses: Dispatch<SetStateAction<ICourse[]>>;
  userPic: string;
  setUserPic: Dispatch<SetStateAction<string>>;
};