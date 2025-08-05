
window.addEventListener("scroll", () => {
const imageZone = document.querySelectorAll(".ima-zone")

    const {scrollTop, clientHeight} = document.documentElement
    
    imageZone.forEach(imgZone => {
        const blogImage = imgZone.querySelector('.blog_image')
        const view = blogImage.getBoundingClientRect().top

        if (scrollTop > (scrollTop + view).toFixed() - clientHeight * 0.80) {
            blogImage.classList.add('blog_image-active')
        }
    })
}) 