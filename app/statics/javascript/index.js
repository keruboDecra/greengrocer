
let independent = document.querySelector('.independent');
let company = document.querySelector('.company');
let independent_form = document.querySelector('.independent_form');
let company_form = document.querySelector('.company_form');

if (independent){
    independent.addEventListener('click', () => {
        company_form.classList.add('hidden');
        independent_form.classList.remove('hidden');
        independent.classList.add('color');
        company.classList.remove('color');
    });
}

if (company){
    company.addEventListener('click', () => {
        company_form.classList.remove('hidden');
        independent_form.classList.add('hidden');
        independent.classList.remove('color');
        company.classList.add('color');
    });
}