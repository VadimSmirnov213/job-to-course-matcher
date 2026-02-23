import { createContext, FC, ReactNode, useState, useContext } from "react";
import { IUser, ICourse, SkillContextType } from "../../@types/types";

export const SkillContext = createContext<SkillContextType>({
    user: null,
    setUser: () => {},
    courses: [],
    setCourses: () => {},
    userPic: "",
    setUserPic: () => {}
});