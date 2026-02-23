import React, { useEffect, useState } from 'react';
import { Route, BrowserRouter, Routes } from "react-router-dom";
import Home from './components/home/Home';

import '@fontsource/roboto/300.css';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Catalogue from './components/catalogue/Catalogue';
import Analysis from './components/analysis/Analysis';
import Profile from './components/profile/Profile';
import Auth from './components/auth/Auth';

import { SkillContext } from './components/context/SkillContext';
import { ICourse, IUser } from './@types/types';
import Reg from './components/reg/Reg';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#262626'
    },
    secondary: {
      main: '#4e4e4e'
    }
  },
});

function App() {
  
  const [user, setUser] = useState<IUser | null>(null);
  const [courses, setCourses] = useState<ICourse[]>([]);
  const [userPic, setUserPic] = useState<string>("");

  return (
    <ThemeProvider theme={darkTheme}>
      <SkillContext.Provider value={{ user, setUser, courses, setCourses, userPic, setUserPic }}>
        <BrowserRouter>
          <Routes>
            <Route path={'/'} element={<Home/>} />
            <Route path={'/catalogue'} element={<Catalogue/>} />
            <Route path={'/analysis'} element={<Analysis/>} />
            <Route path={'/profile'} element={<Profile/>} />
            <Route path={'/auth'} element={<Auth />} />
            <Route path={'/reg'} element={<Reg />} />
           </Routes>
        </BrowserRouter>  
      </SkillContext.Provider>
    </ThemeProvider>
  );
}

export default App;
