const buttonMenu = document.querySelector('.button-menu');
const buttonclose = document.querySelector('.button-close');
const sidebar = document.querySelector('.sidebar');

  //  console.log(buttonMenu)
 //   console.log(sidebar)
 //  console.log(buttonclose)

    buttonMenu.addEventListener("click",() =>{
        if (sidebar.classList.contains('sidebar-active')){
            sidebar.classList.remove('sidebar-active')
        }
        else
        sidebar.classList.add('sidebar-active')
    })

    buttonclose.addEventListener("click",() =>{
        sidebar.classList.remove('sidebar-active')

    }
    )


