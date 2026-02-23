import Sidebar from '../sidebar/Sidebar';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom'
import { useContext, useEffect } from 'react';

import { SkillContext } from '../context/SkillContext';
import { SkillContextType } from '../../@types/types';

import './style.css'

const Home = () => {

  const navigate = useNavigate()

  const context = useContext<SkillContextType>(SkillContext);

  useEffect(() => {
    if(context.user === null) {
      navigate('/auth')
    }
    else {
      // user pic
      fetch(`http://62.113.104.103:9000/api/files/avatars/${context.user?.id}`, {
        method: 'GET',
        mode: 'cors',
        cache: 'no-cache',
        headers: {
          'Content-type': 'image/jpeg'
        }
      })
      .then(
        res => {
          if(res.status == 200) {
            res.blob()
            .then(
              blob => {
                context.setUserPic(URL.createObjectURL(blob))
                localStorage.setItem('userPic', URL.createObjectURL(blob))
              }
            )
          }
        }
      )
    }
  }, [])

  return(
    <div className='container'>
      <Sidebar name="Artjom" surname="Safonov" highlight={0}/>
      <div className='home'>
        <div className='info'>
          <h1><i># SkillSync</i></h1>
          <p>В современном мире образовательные платформы предлагают широкий ассортимент курсов на любой вкус и под любые потребности. Однако из-за такого разнообразия пользователи часто сталкиваются с трудностью в выборе курса, который наилучшим образом соответствует их профессиональным амбициям и карьерным целям. Проблема усугубляется отсутствием эффективных инструментов для анализа и сопоставления персональных карьерных путей с актуальными образовательными предложениями.</p>
          <p>Сервис "SkillSync" разрабатывается для решения этой проблемы, предлагая пользователям инновационный инструмент для подбора образовательных курсов. Цель проекта — создать систему, которая не только упростит процесс выбора курсов, но и обеспечит персонализированный подход к обучению, исходя из индивидуальных карьерных целей и текущих рыночных требований.</p>
          <h1><i># Цели и задачи</i></h1>
          <p>
            Основные функциональности и цели сервиса "SkillSync" включают:
            <ol>
              <li style={{ marginTop: '8px' }}>Анализ требований вакансий</li>
              <ul>
                <li style={{ marginTop: '8px' }}>Разработка алгоритмов, способных анализировать описания вакансий и выделять ключевые навыки и требования, необходимые для каждой специализации.</li>
                <li style={{ marginTop: '8px' }}>Создание базы данных требуемых навыков, которая постоянно обновляется в соответствии с текущими рыночными трендами.</li>
              </ul>
              <li style={{ marginTop: '8px' }}>Персонализированные рекомендации курсов</li>
              <ul>
                <li style={{ marginTop: '8px' }}>Использование современных алгоритмов машинного обучения для адаптации предложений курсов под индивидуальные профили пользователей, их навыки и карьерные амбиции.</li>
                <li style={{ marginTop: '8px' }}>Предоставление пользователю рекомендаций, основанных на синергии его текущих умений и наиболее востребованных навыков на рынке.</li>
              </ul>
              <li style={{ marginTop: '8px' }}>Интерактивные образовательные траектории</li>
              <ul>
                <li style={{ marginTop: '8px' }}>Возможность для пользователей создавать и настраивать свои обучающие пути, включая выбор курсов, которые можно последовательно изучать для достижения карьерных целей.</li>
                <li style={{ marginTop: '8px' }}>Инструменты для мониторинга прогресса и адаптации образовательных планов в ответ на изменения в карьерных ориентирах или рыночной ситуации.</li>
              </ul>
            </ol>
          </p>
          <div style={{ display: 'flex', justifyContent: 'center', borderTop: '1px solid #999999' }}>
            <Button
              sx={{ bgcolor: 'Highlight', textTransform: 'none', color: "#fff", marginTop: '20px' }}
              size='large'
              onClick={() => navigate('/catalogue')}
            >
              Посмотреть курсы
            </Button>
            <Button
              sx={{ bgcolor: 'Highlight', textTransform: 'none', color: "#fff", marginTop: '20px', marginLeft: '20px' }}
              size='large'
              onClick={() => navigate('/analysis')}
            >
              Подобрать курсы
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home;