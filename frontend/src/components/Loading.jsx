import { ProgressSpinner } from 'primereact/progressspinner';

const Loading = () => {
    return(
        <div style={{width: '100%', height: '100%', display: 'flex', justifyContent: 'center'}}>
            <ProgressSpinner style={{marginTop: '20%'}} />
        </div>
    )
}

export default Loading;