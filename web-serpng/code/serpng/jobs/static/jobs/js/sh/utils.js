//
// Add a 'startsWith' function to String object.
//
if (!$.isFunction(String.prototype.startsWith)) {
  String.prototype.startsWith = function(str) {
    return this.slice(0, str.length) === str;
  };
}