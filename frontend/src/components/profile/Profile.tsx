import { useNavigate } from 'react-router-dom'
import { useContext, useEffect, useState } from 'react';
import { styled } from '@mui/material/styles';
import { SkillContext } from '../context/SkillContext';
import { IUser, SkillContextType } from '../../@types/types';
import querystring from 'querystring'

import Avatar from '@mui/material/Avatar';

import './style.css'
import Sidebar from '../sidebar/Sidebar';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

const Profile = () => {

  const navigate = useNavigate()

  const context = useContext<SkillContextType>(SkillContext);

  const [fname, setFname] = useState<string | undefined>(context.user?.first_name);
  const [sname, setSname] = useState<string | undefined>(context.user?.last_name);
  const [age, setAge] = useState<number | undefined>(context.user?.age);
  const [role, setRole] = useState<string | undefined>(context.user?.role);
  const [exp, setExp] = useState<string | undefined>(context.user?.exp);
  const [stack, setStack] = useState<Array<string> | undefined>(context.user?.stack);

  useEffect(() => {
    if(context.user === null) {
      navigate('/auth')
    }
  }, [])

  const handleInputArray = (el: string) => {
    if(stack)
    {
      setStack([...stack, el])
    }
  }

  const handleToStringQueryArray = (array: Array<string> | undefined) => {
    if(!context.user?.stack) {
      return '[""]'
    }
    let str = ""
    if(array)
    {
      str = "["
      array.map((el, index) => {
        if(index == array.length - 1) {
          str += `"${el}"`
        }
        else {
          str += `"${el}",`
        }
      })
      str += "]"
    }
    
    return str
  }

  const handleUpdateUser = () => {
    try {
      let body = JSON.stringify({
        first_name: `${fname}`,
        last_name: `${sname}`,
        age: age,
        role: `${role}`,
        exp: `${exp}`
      })
      body = body.substring(0, body.length - 1);
      let stack_str = `, "stack": ` + `${handleToStringQueryArray(stack)}` + "}";
      body += stack_str

      fetch(`http://62.113.104.103:9000/api/users/${localStorage.getItem('login')}`, {
        method: 'PUT',
        mode: 'cors',
        headers: {
          'Accept': 'application/json',
          'Content-type': 'application/json'
        },
        body: body
      })
      .then(
        resj => { 
          resj.json()
          console.log(body)
        }
      )
    }
    finally { 
      navigate('/profile')
    }
  }

  return(
    <div className='container'>
      <Sidebar name="Artjom" surname="Safonov" highlight={1}/>
      <div className='profile'>
        <div className='info'>
          <div>
            <Avatar alt="" src={context.userPic} sx={{ width: 90, height: 90 }} />
          </div>
          <div className='inputs'>
            <div>
              <InputLabel id="fname" sx={{ fontSize: '12px', color: "#999999" }}>Имя</InputLabel>
              <TextField id="first_name" label="" variant="outlined" value={fname} onChange={(e) => {setFname(e.target.value)}}/>
            </div>
            <div>
              <InputLabel id="fname" sx={{ fontSize: '12px', color: "#999999" }}>Фамилия</InputLabel>
              <TextField id="last_name" label="" variant="outlined" value={sname} onChange={(e) => {setSname(e.target.value)}}/>
            </div>
            <div>
              <InputLabel id="fname" sx={{ fontSize: '12px', color: "#999999" }}>Возраст</InputLabel>
              <TextField id="age" label="" variant="outlined" value={age} onChange={(e) => {setAge(Number(e.target.value))}}/>
            </div>
            <div>
              <InputLabel id="fname" sx={{ fontSize: '12px', color: "#999999" }}>Специализация</InputLabel>
              <TextField id="role" label="" variant="outlined" value={role} onChange={(e) => {setRole(e.target.value)}}/>
            </div>
            <div>
              <InputLabel id="fname" sx={{ fontSize: '12px', color: "#999999" }}>Опыт работы</InputLabel>
              <TextField id="exp" label="" variant="outlined" value={exp} onChange={(e) => {setExp(e.target.value)}}/>
            </div>
            <div>
              <InputLabel id="fname" sx={{ fontSize: '12px', color: "#999999" }}>Навыки</InputLabel>
              <TextField id="stack" label="" variant="outlined" value={stack?.join().split(' ')} onChange={(e) => handleInputArray(e.target.value)}/>
            </div>
          </div>
          <a style={{ color: "#999999", fontSize: '12px', marginTop: '20px',  marginBottom: '20px' }}><i>Введённые вами данные влияют на подборку курсов и рекомендаций в системе</i></a>
          <div style={{ display: 'flex', justifyContent: 'center', borderTop: '1px solid #999999', width: '100%' }}>
            <Button
                component="label"
                role={undefined}
                variant="contained"
                tabIndex={-1}
                startIcon={<CloudUploadIcon />}
                sx={{ bgcolor: 'Highlight', textTransform: 'none', marginTop: '20px'}}
              >
                Загрузить фото
                <VisuallyHiddenInput type="file" accept="image/png, image/jpeg"/>
              </Button>
            <Button
              sx={{ bgcolor: 'Highlight', textTransform: 'none', color: "#fff", marginTop: '20px', marginLeft: '20px' }}
              onClick={() => handleUpdateUser()}
            >
              Сохранить
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile;