import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import './style.css'
import { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { IUser, SkillContextType } from '../../@types/types';
import { SkillContext } from '../context/SkillContext';

const Reg = () => {

  const [login, setLogin] = useState<string>();
  const [pass, setPass] = useState<string>();

  const navigate = useNavigate();

  const context = useContext<SkillContextType>(SkillContext);

  const handleReg = () => {
    let status = 0
    fetch(`http://62.113.104.103:9000/api/users`, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Accept': 'application/json',
        'Content-type': 'application/json'
      },
      body: JSON.stringify({
        login: `${login}`,
        password: `${pass}`,
        schema: {
          first_name: "",
          last_name: "",
          age: 0,
          role: "",
          exp: "",
          stack: [""]
        }
        })
    })
    .then(
      res => {
        if(res.status === 201) {
          navigate('/auth')
        }
      }
    )
  }

  return(
    <div className='reg'>
      <div className='info'>
        <div className='header'>
          <h1>Регистрация</h1>
        </div>
        <div className='inputs'>
          <TextField id="outlined-basic" label="Логин" variant="outlined" onChange={(e) => setLogin(e.target.value)}/>
          <br />
          <TextField id="outlined-basic" label="Пароль" variant="outlined" type="password" onChange={(e) => setPass(e.target.value)}/>
        </div>
        <Button sx={{ bgcolor: 'green', textTransform: 'none', color: "#fff", mt: 2 }} size='large' onClick={() => handleReg()}>
          Создать аккаунт
        </Button>
      </div>
    </div>
  )
}

export default Reg;