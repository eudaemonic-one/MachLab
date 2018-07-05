document.getElementByClass("panel").addEventListener("click", function () {
    document.getElementById("demo").innerHTML = "Hello World";
});

function toggleSubitems(o) {
    o.children.toggle()
}
