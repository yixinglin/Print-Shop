

const PDFViewer = ({ title, url, width, height }) => {
    return(
    <div>
        <h2>{title}</h2>
        <iframe
            src={url}
            width={width}
            height={height}
            style={{ border: 'solid 1px' }}
            title="PDF Viewer"
        />
    </div>
    )

}

const PDFB64Viewer = (b64) => {

}




export default PDFViewer;