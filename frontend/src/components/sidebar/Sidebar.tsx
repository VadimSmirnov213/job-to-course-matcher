import './style.css';
import { Box, Button, TextField } from '@mui/material';
import WorkHistoryIcon from '@mui/icons-material/WorkHistory';
import { useNavigate } from 'react-router-dom'
import Avatar from '@mui/material/Avatar';

import SearchIcon from '@mui/icons-material/Search';
import LogoutIcon from '@mui/icons-material/Logout';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import LayersOutlinedIcon from '@mui/icons-material/LayersOutlined';
import PersonOutlinedIcon from '@mui/icons-material/PersonOutlined';
import WorkHistoryOutlinedIcon from '@mui/icons-material/WorkHistoryOutlined';

import { SkillContextType } from '../../@types/types';
import { SkillContext } from '../context/SkillContext';
import { useContext } from 'react';

interface ISidebarProps {
  highlight: number;
  name: string;
  surname: string;
}

const Sidebar = ({highlight, name, surname} : ISidebarProps) => {
  
  const navigate = useNavigate()

  const context = useContext<SkillContextType>(SkillContext);

  function stringToColor(string: string) {
    let hash = 0;
    let i;
  
    /* eslint-disable no-bitwise */
    for (i = 0; i < string.length; i += 1) {
      hash = string.charCodeAt(i) + ((hash << 5) - hash);
    }
  
    let color = '#';
  
    for (i = 0; i < 3; i += 1) {
      const value = (hash >> (i * 8)) & 0xff;
      color += `00${value.toString(16)}`.slice(-2);
    }
    /* eslint-enable no-bitwise */
  
    return color;
  }
  
  function stringAvatar(name: string) {
    return {
      sx: {
        bgcolor: stringToColor(name),
      },
      children: `${name.split(' ')[0][0]}${name.split(' ')[1][0]}`,
    };
  }

  const handleLogout = () => {
   context.setUser(null);
   localStorage.setItem('login', '')
   localStorage.setItem('pass', '')
   navigate('/auth')
  }

  return(
    <div className='sidebar'>
      
      <Box sx={{ display: 'flex', alignItems: 'center', mt: '15px', color: '#fff', marginTop: '40px'}}>
        {/* <Avatar {...stringAvatar(name + " " + surname)}/> */}
        <Avatar src={context.userPic}/>
        <a style={{ marginLeft: '10px' }}>{context.user?.first_name}</a>
        <a style={{ marginLeft: '5px' }}>{context.user?.last_name}</a>
      </Box>

      {/* <Box sx={{ display: 'flex', alignItems: 'flex-end'}}>
        <SearchIcon sx={{ color: 'action.active', mr: 1, my: 0.5 }} />
        <TextField id="input-with-sx" label="Поиск..." variant="standard" />
      </Box> */}

      <Button 
        variant={ highlight === 0 ? "contained" : "text"}
        onClick={() => navigate('/')}
        sx={{ textTransform: 'none', color: highlight === 0 ? "#fff" : "#999999", boxShadow: 'none', marginTop: '10px' }}
      >
        <HomeOutlinedIcon sx={{ color: highlight === 0 ? "#fff" : "#999999", mr: 1, my: 0.5 }} />
        <a style={{ color: highlight === 0 ? "#fff" : "#999999"  }}>Главная</a>
      </Button>
      <Button 
        variant={ highlight === 1 ? "contained" : "text"}
        onClick={() => navigate('/profile')}
        sx={{ textTransform: 'none', color: highlight === 1 ? "#fff" : "#999999", boxShadow: 'none'  }}
      >
        <PersonOutlinedIcon sx={{ color: highlight === 1 ? "#fff" : "#999999", mr: 1, my: 0.5 }} />
        <a style={{ color: highlight === 1 ? "#fff" : "#999999"  }}>Личный кабинет</a>
      </Button>
      <Button 
        variant={ highlight === 2 ? "contained" : "text"}
        onClick={() => navigate('/catalogue')}
        sx={{ textTransform: 'none', color: highlight === 2 ? "#fff" : "#999999", boxShadow: 'none'  }}
      >
        <LayersOutlinedIcon sx={{ color: highlight === 2 ? "#fff" : "#999999", mr: 1, my: 0.5 }} />
        <a style={{ color: highlight === 2 ? "#fff" : "#999999"  }}>Каталог</a>
      </Button>
      <Button 
        variant={ highlight === 3 ? "contained" : "text"}
        onClick={() => navigate('/analysis')}
        sx={{ textTransform: 'none', color: highlight === 3 ? "#fff" : "#999999", boxShadow: 'none'  }}
      >
        <WorkHistoryOutlinedIcon sx={{ color: highlight === 3 ? "#fff" : "#999999", mr: 1, my: 0.5 }} />
        <a style={{ color: highlight === 3 ? "#fff" : "#999999"  }}>Анализ вакансий</a>
      </Button>

      <div className='footer'>
        <Button variant="contained" sx={{ textTransform: 'none' }} onClick={() => handleLogout()}> 
          <LogoutIcon sx={{ color: '#999999', mr: 1, my: 0.5 }}/>
          <a style={{ color: '#999999' }}>Выйти</a>
        </Button>
      </div>

    </div>
  )
}

export default Sidebar;