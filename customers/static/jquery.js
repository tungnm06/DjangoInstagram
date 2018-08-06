function myFunction(){
$(".searchform").submit();


}

 $(document).ready(function() {
       $(".searchform").on("submit",function(e){
           e.preventDefault();
           var form = $(this);
           $.post(form.attr('action'), form.serialize())
              .done(function(customer_dict) {
                $(".hienthi").empty()
                for (i in customer_dict.customer) {

                    $(".hienthi").append(
                      '<img width="30px" height="30px" src="/media/' + customer_dict.customer[i].avarta+'">' + "  "+
                    '<a href="/customers/detail/'+customer_dict.customer[i].id+'">' + customer_dict.customer[i].fullname +'</a>'+'<br>'
                    )
}
})
           })
           });
