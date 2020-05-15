package repl

// IPythonSession todo
type IPythonSession struct {
	Session
}

// NewIPythonSession todo
func NewIPythonSession() *IPythonSession {
	return &IPythonSession{}
}

// Send todo
func (s *IPythonSession) Send(line []byte) []byte {

	return []byte{}
}
