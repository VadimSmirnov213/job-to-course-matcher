import Sidebar from '../sidebar/Sidebar';
import CourseCard from '../ui/CourseCard';
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import TextField from '@mui/material/TextField';

import { useNavigate } from 'react-router-dom'
import { useContext, useEffect, useState } from 'react';

import { SkillContext } from '../context/SkillContext';
import { ICourse, SkillContextType } from '../../@types/types';

import './style.css'

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

interface IRec {
  course_name: string;
  course_description: string;
  course_id: number;
  course_rating: number;
}

const Analysis = () =>
{

  const navigate = useNavigate()

  const context = useContext<SkillContextType>(SkillContext);
  
  const [recs, setRecs] = useState<IRec[]>([])
  const [top, setTop] = useState<number>(5);
  const [url, setUrl] = useState<string>("");

  useEffect(() => {
    if(context.user === null) {
      navigate('/auth')
    }
  }, [])

  const handlePredict = () => {
    fetch(`http://62.113.104.103:9000/api/predict/recommendation?top=${top}&url=${url}`)
    .then(
      res => res.json()
    )
    .then(
      data => setRecs(data.recommendations)
    )
  }

  return(
    <div className='container'>
    <Sidebar name="Artjom" surname="Safonov" highlight={3}/>
    <div className='analysis'>
      <div className='options'>
        <h2 style={{ color: "#fff", margin: 0 }}>Выбор вакансии</h2>
        <a style={{ color: "#999999" }}>Загрузите файл с информацией о вакансии или кратко опишите её</a>
      </div>
      <div className='info'>
        <div className='vac'>
          {/* <div className='header' style={{ backgroundColor: '#1e1e1e', textAlign: 'center'}}>
            <h3 style={{ margin: '7px' }}>Выберите вакансию</h3>
          </div> */}
          <div className='inputinfo'>
            {/* <a>Бокс с вакансией</a> */}
            <TextField id="outlined-basic" label="Ссылка на вакансию" variant="outlined" multiline rows={6} value={url} onChange={(e) => setUrl(e.target.value)}/>
            <div style={{ display: 'flex', columnGap: '15px' }}>
              {/* <Button
                component="label"
                role={undefined}
                variant="contained"
                tabIndex={-1}
                startIcon={<CloudUploadIcon />}
                sx={{ bgcolor: 'Highlight', textTransform: 'none'}}
              >
                Загрузить файл
                <VisuallyHiddenInput type="file" />
              </Button> */}
              <TextField
                id="outlined-number"
                label="Количество"
                type="number"
                InputLabelProps={{
                  shrink: true,
                }}
                defaultValue={5}
                value={top}
                onChange={(e) => setTop(Number(e.target.value))}
              />
              <Button
                sx={{ bgcolor: 'Highlight', textTransform: 'none', color: "#fff" }}
                onClick={() => handlePredict()}
              >  
                Подобрать
              </Button>
            </div>
          </div>
        </div>
        <div className='options'>
          <h2 style={{ color: "#fff", margin: 0 }}>Рекомендации</h2>
          <a style={{ color: "#999999" }}>Вот что мы нашли для вас</a>
        </div>
        <div className='gallery'>
          {
            recs.map((course, index) => {
              return <CourseCard key={index} title={course.course_name} info={course.course_description}  id={course.course_id} rating={course.course_rating}/>
            })
          }
          {/* <CourseCard title="Фуллстак за 5 дней" info="Вау!" spec="Fullstack"/>
          <CourseCard title="React всего за {dayCount} дней" info="Реакт и реакт и рекат..." spec="React Frontend Web"/>
          <CourseCard title="Только для умных" info="Based and red pilled" spec="C C++ D Rust"/>
          <CourseCard title="Фуллстак за 5 дней" info="Вау!" spec="Fullstack"/>
          <CourseCard title="React всего за {dayCount} дней" info="Реакт и реакт и рекат..." spec="React Frontend Web"/>
          <CourseCard title="Только для умных" info="Based and red pilled" spec="C C++ D Rust"/> */}
        </div>
      </div>
    </div>
  </div>
  )
}

export default Analysis;