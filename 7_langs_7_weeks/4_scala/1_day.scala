// DAY 1


def whileLoop {
  println("while loop")
  var i = 1
  while(i <= 3) {
    println(i)
    i += 1
  }
}

whileLoop


def forLoop {
  println("for loop using Java-style iteration")
  for(i <- 0 until args.length) {
    println(args(i))
  }
}

forLoop


def rubyStyleForLoop {
  println("for loop using ruby style iteration")
  args.foreach { arg =>
    println(arg)
  }
}

rubyStyleForLoop


// Ranges and Tuples

val range = 0 until 10
println(range.start)
println(range.end)
println(range.step)

println((0 to 10) by 5)
println((0 to 10) by 6)

println((10 until 0) by - 1)

// val range = 'a' to 'e'

val person = ("Elvis", "Presley")
println(person._1)
println(person._2)

val (x, y) = (1, 2)


// Classes

class Person(firstName: String, lastName: String)

val gump = new Person("Foresst", "Gump")
println(gump)

class Compass {
  // constructor
  val directions = List("north", "east", "south", "west")
  var bearing = 0

  print("Initial bearing: ")
  println(direction)

  def direction() = directions(bearing)  // one line method without braces

  def inform(turnDirection: String) {
    println("Turning " + turnDirection + ". Now brearing " + direction)
  }

  def turnRight() {
    bearing = (bearing + 1) % directions.size
    inform("right")
  }

  def turnLeft() {
    bearing = (bearing + (directions.size - 1)) % directions.size
    inform("left")
  }

}

val myCompass = new Compass

myCompass.turnRight
myCompass.turnRight

myCompass.turnLeft
myCompass.turnLeft
myCompass.turnLeft


class PersonZ(first_name: String) {
  println("Outer constructor")
  def this(first_name: String, last_name: String) {
    this(first_name)
    println("Inner constructor")
  }
  def talk() = println("Hi")
}

val bob = new PersonZ("Bob")
val bobTate = new PersonZ("Bob", "Tate")


object TrueRing {
  def rule = println("To rule them all")
}

TrueRing.rule


class PersonI(val name: String) {
  def talk(message: String) = println(name + " says " + message)
  def id(): String = name
}

class Employee(override val name: String,
                        val number: Int) extends PersonI(name) {
  override def talk(message: String) {
    println(name + " with number " + number + " says " + message)
  }
  override def id():String = number.toString
}

val employee = new Employee("Yoda", 4)
employee.talk("Blabla blal bsdfsf")

class PersonA(val name:String)

trait Nice {
  def greet() = println("Howdy partner.")
}

class Character(override val name:String) extends PersonA(name) with Nice

val flanders = new Character("Ned")
flanders.greet


// HOMEWORK

// tic-tac-toe
class TBoard {
  val markers = Array("O", "X")
  var board = Array.fill(9){"."}
  var playing = true
  var currentMarker = "O"

  def showBoard() {
    println(s"| ${board(0)} | ${board(1)} | ${board(2)} |")
    println("-------------")
    println(s"| ${board(3)} | ${board(4)} | ${board(5)} |")
    println("-------------")
    println(s"| ${board(6)} | ${board(7)} | ${board(8)} |")
    println("")
  }

  def changeMarker() {
    if (currentMarker == "O") {
      currentMarker = "X"
    } else {
      currentMarker = "O"
    }
  }

  def putMark(position: Integer) {
    if ((position < 1) || (position > 9)) {
      println("Position out of range")
    } else if (board(position-1) != "."){
      println("Position occupied!")
    } else {
      board(position-1) = currentMarker

      checkStatus()
      changeMarker()
    }
  }

  def checkStatus() {
    if (board.count(_ == ".") == 0) {
      playing = false
      println("DRAW")
    } else if (
      (board.slice(0,3).count(_ == currentMarker) == 3) ||
      (board.slice(3,6).count(_ == currentMarker) == 3) ||
      (board.slice(6,9).count(_ == currentMarker) == 3) ||
      (Array(board(0), board(3), board(6)).count(_ == currentMarker) == 3) ||
      (Array(board(1), board(4), board(7)).count(_ == currentMarker) == 3) ||
      (Array(board(2), board(5), board(8)).count(_ == currentMarker) == 3) ||
      (Array(board(0), board(4), board(8)).count(_ == currentMarker) == 3) ||
      (Array(board(2), board(4), board(6)).count(_ == currentMarker) == 3)
    ){
      playing = false
      println(s"The winner is: '${currentMarker}'!")
    }

  }

}

val MyBoard = new TBoard

MyBoard.showBoard

MyBoard.putMark(0)

MyBoard.showBoard

MyBoard.putMark(0)

MyBoard.putMark(1)

MyBoard.showBoard

println(MyBoard.playing)

MyBoard.putMark(4)
MyBoard.putMark(7)

MyBoard.putMark(11)

MyBoard.showBoard

println(MyBoard.playing)

println(MyBoard.checkStatus)

// ---

val aba = Array("a", "b", "C")

println(s"${aba.slice(1,2)}")


val PlayBoard = new TBoard
PlayBoard.showBoard

while (PlayBoard.playing) {
  println(s"Choose position for '${PlayBoard.currentMarker}'")
  PlayBoard.putMark(scala.io.StdIn.readLine().toInt)
  PlayBoard.showBoard
}
